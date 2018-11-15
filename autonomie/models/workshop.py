# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
import logging

from sqlalchemy import (
    Integer,
    Column,
    ForeignKey,
    String,
    DateTime,
    Boolean,
    Table,
    Text,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)

from autonomie_base.models.base import (
    default_table_args,
    DBBASE,
)
from autonomie_base.models.types import JsonEncodedList
from autonomie.models.activity import Event


log = logging.getLogger(__name__)


WORKSHOP_TRAINER = Table(
    'workshop_trainer',
    DBBASE.metadata,
    Column("workshop_id", Integer, ForeignKey("workshop.id", ondelete="cascade"), nullable=False),
    Column("user_id", Integer, ForeignKey("accounts.id", ondelete="cascade"), nullable=False),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


class Workshop(Event):
    """
    A workshop model

    It's a meta event grouping a bunch of timeslots with each their own
    attendance sheet
    """
    __tablename__ = 'workshop'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'workshop'}
    id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    # Libellé pour la sortie pdf
    #info1 = Column(String(125), default="")
    #info2 = Column(String(125), default="")
    #info3 = Column(String(125), default="")
    info1_id = Column(ForeignKey('workshop_action.id'))
    info2_id = Column(ForeignKey('workshop_action.id'))
    info3_id = Column(ForeignKey('workshop_action.id'))
    info1 = relationship(
        "WorkshopAction",
        primaryjoin="Workshop.info1_id==WorkshopAction.id",
    )
    info2 = relationship(
        "WorkshopAction",
        primaryjoin="Workshop.info2_id==WorkshopAction.id",
    )
    info3 = relationship(
        "WorkshopAction",
        primaryjoin="Workshop.info3_id==WorkshopAction.id",
    )
    trainers = relationship(
        "User",
        secondary=WORKSHOP_TRAINER,
        info={
            'colanderalchemy': {
                'title': u"Animateur(s)/ice(s)",
            },
            'export': {'exclude': True},
        }
    )
    description = Column(Text, default='')

    @property
    def title(self):
        """
        Return a title for this given workshop
        """
        return u"Atelier '{0}' animé par {1}".format(
            self.name, ', '.join(i.label for i in self.trainers))

    def duplicate(self):
        new_item = Workshop(
            name=self.name,
            description=self.description,
            _acl=self._acl,
            datetime=self.datetime,
            status=self.status,
            info1=self.info1,
            info2=self.info2,
            info3=self.info3,
            trainers=self.trainers,
            signup_mode=self.signup_mode,
            owner=self.owner,
        )

        for timeslot in self.timeslots:
            new_item.timeslots.append(timeslot.duplicate())

        for participant in self.participants:
            new_item.participants.append(participant)

        return new_item

    def relates_single_day(self):
        """
        Does the TimeSlots are all occuring the same day as Workshop.
        """
        for slot in self.timeslots:
            if (
                    slot.start_time.date() != self.datetime.date()
                    or
                    slot.end_time.date() != self.datetime.date()
            ):
                return False
        return True

    def __str__(self):
        return "<Workshop : %s>" % (self.id,)

    def __unicode__(self):
        return u"<Workshop : %s (%s)>" % (self.id, self.title)


class Timeslot(Event):
    """
    A time slot for a given workshop
    """
    __tablename__ = 'timeslot'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'timeslot'}
    id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    start_time = Column(DateTime())
    end_time = Column(DateTime())
    workshop_id = Column(ForeignKey('workshop.id'))

    workshop = relationship(
        'Workshop',
        primaryjoin="Timeslot.workshop_id==Workshop.id",
        backref=backref(
            'timeslots',
            order_by='Timeslot.start_time',
            cascade='all, delete-orphan'
            ),
        )

    @property
    def duration(self):
        time_delta = self.end_time - self.start_time
        hours, rest = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(rest, 60)
        hours = 24 * time_delta.days + hours
        return hours, minutes

    def duplicate(self):
        timeslot = Timeslot(
            name=self.name,
            _acl=self._acl,
            datetime=self.datetime,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        for participant in self.participants:
            timeslot.participants.append(participant)

        return timeslot


class WorkshopAction(DBBASE):
    __tablename__ = 'workshop_action'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    label = Column(String(255))
    active = Column(Boolean(), default=True)
    parent_id = Column(ForeignKey("workshop_action.id"))
    children = relationship(
        "WorkshopAction",
        primaryjoin="WorkshopAction.id==WorkshopAction.parent_id",
        backref=backref("parent", remote_side=[id]),
        cascade="all",
    )
