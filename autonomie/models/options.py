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
Base tools for administrable options
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.util import classproperty

from autonomie.utils.ascii import camel_case_to_name
from autonomie.forms import (
    get_hidden_field_conf,
    EXCLUDED,
)
from autonomie.models.base import (
    DBBASE,
    default_table_args,
)



class ConfigurableOption(DBBASE):
    """
    Base class for options
    """
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()}
    )
    label = Column(
        String(100),
        info={'colanderalchemy': {'title': u'Libellé'}},
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalchemy': EXCLUDED}
    )
    order = Column(
        Integer,
        default=0,
        info={'colanderalchemy': EXCLUDED}
    )
    type_ = Column(
        'type_',
        String(30),
        nullable=False,
        info={'colanderalchemy': EXCLUDED}
        )

    @classproperty
    def __mapper_args__(cls):
        name = cls.__name__
        if name == 'ConfigurableOption':
            return {
                'polymorphic_on': 'type_',
                'polymorphic_identity':'configurable_option'
            }
        else:
            return {'polymorphic_identity': camel_case_to_name(name)}

    @classmethod
    def query(cls, *args):
        query = super(ConfigurableOption, cls).query(*args)
        query = query.filter(ConfigurableOption.active==True)
        query = query.order_by(ConfigurableOption.order)
        return query


def get_id_foreignkey_col(foreignkey_str):
    """
    Return an id column as a foreignkey with correct colander configuration

        foreignkey_str

            The foreignkey our id is pointing to
    """
    column = Column(
        "id",
        Integer,
        ForeignKey(foreignkey_str),
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()},
    )
    return column


