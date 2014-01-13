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
"""
    Models related to activities :

        Activity Types
        Activities
"""
import logging
import datetime

from sqlalchemy import (
    Table,
    Integer,
    Column,
    ForeignKey,
    String,
    Date,
    Enum,
    Text,
    Boolean,
    )
from sqlalchemy.orm import (
    deferred,
    relationship,
    backref,
    )


from autonomie.models.base import (
    DBBASE,
    default_table_args,
    )
from autonomie.models.node import Node


log = logging.getLogger(__name__)


ACTIVITY_PARTICIPANT = Table(
    "activity_participant",
    DBBASE.metadata,
    Column("activity_id", ForeignKey('activity.id')),
    Column("account_id", ForeignKey('accounts.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'])


ACTIVITY_MODES = (u"en direct", u"par mail", u"par courrier", u"par téléphone")


ACTIVITY_STATUS = (u"planned", u"closed",)


class Event(Node):
    """
        An event model
    """
    __tablename__ = 'event'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'event'}
    id = Column(Integer, ForeignKey('node.id'), primary_key=True)
    date = Column(Date, default=datetime.date.today)
    status = Column(String(15), default='planned')


class Activity(Event):
    """
        An activity model
    """
    __tablename__ = 'activity'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'activity'}
    id = Column(Integer, ForeignKey('event.id'), primary_key=True)
    conseiller_id = Column(ForeignKey('accounts.id'))
    type_id = Column(ForeignKey('activity_type.id'))
    mode = Column(Enum(*ACTIVITY_MODES))
    # Champ text multiligne pour les activités
    point = deferred(Column(Text()))
    objectifs = deferred(Column(Text()))
    action = deferred(Column(Text()))
    documents = deferred(Column(Text()))

    type_object = relationship(
            "ActivityType",
            primaryjoin="Activity.type_id==ActivityType.id",
            uselist=False,
            foreign_keys=type_id)
    conseiller = relationship(
            "User",
            primaryjoin="User.id==Activity.conseiller_id",
            backref=backref("managed_activities", order_by="Activity.date")
            )
    participants = relationship(
            "User",
            secondary=ACTIVITY_PARTICIPANT,
            backref="activities",
            )


class ActivityType(DBBASE):
    __tablename__ = 'activity_type'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    label = Column(String(100))
    active = Column(Boolean(), default=True)
