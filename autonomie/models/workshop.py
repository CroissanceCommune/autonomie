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
import datetime

from sqlalchemy import (
    Table,
    Integer,
    Column,
    ForeignKey,
    String,
    Date,
    DateTime,
    )
from sqlalchemy.orm import (
    relationship,
    backref,
    )

from sqlalchemy.ext.associationproxy import association_proxy

from autonomie.models.base import (
    DBBASE,
    default_table_args,
    )
from autonomie.models.types import JsonEncodedList
from autonomie.models.activity import Event


log = logging.getLogger(__name__)


STATUS = (
    ('registered', u'Attendu', ),
    ('attended', u'Présent', ),
    ('absent', u'Absent', ),
    ('cancelled', u'Excusé', ),
    )

WORKSHOP_PARTICIPANT = Table(
    "workshop_participant",
    DBBASE.metadata,
    Column("workshop_id", ForeignKey("workshop.id"), primary_key=True),
    Column("account_id", ForeignKey('accounts.id'), primary_key=True),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


class Workshop(Event):
    """
    A workshop model
    """
    __tablename__ = 'workshop'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'workshop'}
    id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    # Libellé pour la sortie pdf
    info1 = Column(String(125), default="")
    info2 = Column(String(125), default="")
    info3 = Column(String(125), default="")
    leaders = Column(JsonEncodedList)
    date = Column(Date(), default=datetime.date.today())

    participants = relationship(
            "User",
            secondary=WORKSHOP_PARTICIPANT,
            backref=backref(
                "workshops",
                order_by='Workshop.date',
            )
        )


class TimeSlot(Event):
    """
    A given time slot for a workshop
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
        primaryjoin="TimeSlot.workshop_id==Workshop.id",
        backref=backref(
            'timeslots',
            order_by='TimeSlot.start_time',
            cascade='all, delete-orphan'
            ),
        )

    participants = association_proxy('attendances', 'user')


class Attendance(DBBASE):
    """
    Relationship table used to store the attendance of the user's for a given
    timeslot
    """
    __tablename__ = 'attendance'
    account_id = Column(ForeignKey('accounts.id'), primary_key=True)
    timeslot_id = Column(ForeignKey('timeslot.id'), primary_key=True)
    status = Column(String(15), default="registered")

    timeslot = relationship(
        'TimeSlot',
        backref=backref(
            'attendances',
            cascade='all, delete-orphan',
        )
    )
    user = relationship(
        "User",
        backref=backref('workshop_attendances', cascade='all, delete-orphan')
    )

    # Used as default creator function by the association_proxy
    def __init__(self, user):
        self.user = user
