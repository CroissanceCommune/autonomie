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
Models related to statistics

- Sheets
  |- Entries
     |-Criterions


A sheet groups a number of statistics entries.
Each entry is compound of a list of criterions.
"""
import colander
import string
import random
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
    Column,
    DateTime,
    Date,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)

from autonomie.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.models.types import (
    JsonEncodedList,
    ACLType,
    MutableList,
    # PersistentACLMixin,
)
from autonomie import forms
from autonomie.utils import ascii


class StatisticSheet(DBBASE):  # , PersistentACLMixin):
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(),
        info={'colanderalchemy': forms.EXCLUDED},
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime(),
        info={'colanderalchemy': forms.EXCLUDED},
        default=datetime.now(),
        onupdate=datetime.now()
    )
    title = Column(String(255))
    active = Column(Boolean(), default=True)
    _acl = Column(
        MutableList.as_mutable(ACLType),
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            title=self.title,
            active=self.active,
        )

    def duplicate(self):
        new_sheet = StatisticSheet(
            title=u"{0} {1}".format(
                self.title,
                ''.join(
                    random.choice(
                        string.ascii_uppercase + string.digits
                    ) for _ in range(5)
                )
            )
        )
        for entry in self.entries:
            new_sheet.entries.append(entry.duplicate())
        return new_sheet


class StatisticEntry(DBBASE):  # , PersistentACLMixin):
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text())
    _acl = Column(
        MutableList.as_mutable(ACLType),
    )
    sheet_id = Column(ForeignKey('statistic_sheet.id', ondelete='cascade'))
    sheet = relationship(
        "StatisticSheet",
        backref=backref("entries"),
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
        )

    def duplicate(self):
        entry = StatisticEntry(
            title=self.title,
            description=self.description
        )
        for criterion in self.criteria:
            entry.criteria.append(criterion.duplicate())
        return entry


class BaseStatisticCriterion(DBBASE):
    """
    Statistic criterion
    :param str key: The key allows us to match the column we will build a query
    on through the inspector's columns dict (ex: 'coordonnees_lastname' or
    'activity_companydatas.name')
    :param str method: The search method (eq, lte, gt ...)
    :param str search1: The first value we search on
    :param str search2: The second value we search on (in case of range search)
    :param str searches: The list of value we will query on (in case of 'oneof'
    search)
    :param str type: string/number/optrel/date says us which query generator we
    will use
    """
    __table_args__ = default_table_args
    __mapper_args__ = {
        'polymorphic_on': 'type_',
        'polymorphic_identity': 'base',
    }

    id = Column(Integer, primary_key=True)
    key = Column(String(255))
    method = Column(String(25))
    type = Column(String(10))
    type_ = Column(
        'type_',
        String(30),
        info={'colanderalchemy': forms.EXCLUDED},
        nullable=False,
    )
    entry_id = Column(ForeignKey('statistic_entry.id', ondelete='cascade'))
    entry = relationship(
        "StatisticEntry",
        backref=backref("criteria"),
    )

    def __json__(self, request):
        return dict(
            id=str(self.id),
            value=str(self.id),
            key=self.key,
            method=self.method,
            type=self.type,
            entry_id=self.entry_id,
        )


class BoolStatisticCriterion(BaseStatisticCriterion):
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'bool'}
    id = Column(ForeignKey('base_statistic_criterion.id'), primary_key=True)

    def duplicate(self):
        return BoolStatisticCriterion(
            key=self.key,
            method=self.method,
            type=self.type,
        )


class CommonStatisticCriterion(BaseStatisticCriterion):
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'common'}
    id = Column(ForeignKey('base_statistic_criterion.id'), primary_key=True)
    search1 = Column(String(255), default="")
    search2 = Column(String(255), default="")

    def __json__(self, request):
        res = BaseStatisticCriterion.__json__(self, request)
        res.update(dict(
            search1=self.search1,
            search2=self.search2,
        ))
        return res

    def duplicate(self):
        return CommonStatisticCriterion(
            key=self.key,
            method=self.method,
            type=self.type,
            search1=self.search1,
            search2=self.search2,
        )


def list_of_integers_validator(node, value):
    """
    Colander Validator ensuring we've got a list of integers
    """
    if not isinstance(value, list):
        raise colander.Invalid(node, u"Doit être une liste")
    for val in value:
        if not ascii.isint(val):
            raise colander.Invalid(node, u"Ne doit contenir que des nombres")


class OptListStatisticCriterion(BaseStatisticCriterion):
    """
    An Statistic criterion pointing to options ids stored in another table
    """
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'optlist'}
    id = Column(ForeignKey('base_statistic_criterion.id'), primary_key=True)
    searches = Column(
        JsonEncodedList(),
        info={
            'colanderalchemy': {
                'typ': colander.List(),
                'validator': list_of_integers_validator,
            }
        }
    )

    def __json__(self, request):
        res = BaseStatisticCriterion.__json__(self, request)
        res.update(dict(
            searches=self.searches,
        ))
        return res

    def duplicate(self):
        return OptListStatisticCriterion(
            key=self.key,
            method=self.method,
            type=self.type,
            searches=self.searches,
        )


class DateStatisticCriterion(BaseStatisticCriterion):
    """
    Statistic criterion for dates
    :param str key: The key allows us to match the column we will build a query
    on through the inspector's columns dict (ex: 'coordonnees_lastname' or
    'activity_companydatas.name')
    :param str method: The search method (eq, lte, gt ...)
    :param str search1: The first value we search on
    :param str search2: The second value we search on (in case of range search)
    :param str type: string/number/optrel/date says us which query generator we
    will use
    """
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'date'}
    id = Column(ForeignKey('base_statistic_criterion.id'), primary_key=True)
    search1 = Column(Date(), default="")
    search2 = Column(Date(), default="")

    def __json__(self, request):
        res = BaseStatisticCriterion.__json__(self, request)
        res.update(dict(
            search1=self.search1,
            search2=self.search2,
        ))
        return res

    def duplicate(self):
        return DateStatisticCriterion(
            key=self.key,
            method=self.method,
            type=self.type,
            search1=self.search1,
            search2=self.search2,
        )
