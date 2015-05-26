# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
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
Models related to competence evaluation
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
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

from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)


class CompetenceDeadline(ConfigurableOption):
    __colanderalchemy_config__ = {
        'title': u"Échéances",
        'validation_msg': u"Les échéances ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class CompetenceScale(ConfigurableOption):
    __colanderalchemy_config__ = {
        'title': u"Barêmes",
        'validation_msg': u"Les barêmes ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')
    value = Column(
        Integer,
        info={
            'colanderalchemy': {
                'title': u"Valeur",
                'description': u"Valeurs utilisées comme unité dans \
les graphiques",
            }
        }
    )


class CompetenceRequirement(DBBASE):
    """
    Relationship table used to store the requirements for competences
    """
    __table_args__ = default_table_args
    competence_id = Column(ForeignKey('competence.id'), primary_key=True)
    scale_id = Column(ForeignKey('scale.id'))
    deadline_id = Column(ForeignKey('deadline.id'), primary_key=True)

    competence = relationship(
        'Competence',
        backref=backref(
            'requirements',
            cascade='all, delete-orphan',
        ),
    )
    _scale = relationship('Scale')
    _deadline = relationship('Deadline')
    scale = association_proxy('_scale', 'label')
    deadline = association_proxy('_deadline', 'label')


class CompetenceOption(DBBASE):
    """
    A competence model (both for the main one and the sub-competences)

    :param int required_id: The id of the bareme element needed
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    label = Column(String(255))
    active = Column(Boolean(), default=True)
    parent_id = Column(ForeignKey("competence.id"))
    children = relationship(
        "Competence",
        primaryjoin="Competence.id==Competence.parent_id",
        backref=backref("parent", remote_side=[id]),
        cascade="all",
    )

    @classmethod
    def query(cls, active=True):
        query = super(Competence, cls).query()
        query = query.filter_by(active=active)
        return query
