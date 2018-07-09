# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
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
#
"""
    Nodes model is a base model for many other models (projects, documents,
    files, events)
    This way we can easily use the parent/children relationship on an agnostic
    way as in a CMS
"""
import colander
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref

from autonomie_base.models.types import (
    ACLType,
    PersistentACLMixin,
    MutableList,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)


class Node(DBBASE, PersistentACLMixin):
    """
    A base node providing a parent<->children structure for most of the models
    (usefull for file attachment)
    """
    __tablename__ = 'node'
    __table_args__ = default_table_args
    __mapper_args__ = {
        'polymorphic_on': 'type_',
        'polymorphic_identity': 'nodes',
    }
    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Nom",
                "missing": colander.required,
            },
        },
        nullable=True,
    )

    created_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Créé(e) le",
            }
        },
        default=datetime.now,
    )

    updated_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Mis(e) à jour le",
            }
        },
        default=datetime.now,
        onupdate=datetime.now
    )

    parent_id = Column(
        ForeignKey('node.id'),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
    )

    children = relationship(
        'Node',
        primaryjoin='Node.id==Node.parent_id',
        backref=backref(
            'parent',
            remote_side=[id],
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True},
            },
        ),
        cascade='all',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
    )
    files = relationship(
        "File",
        primaryjoin="Node.id==File.parent_id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
    )

    type_ = Column(
        'type_',
        String(30),
        info={'colanderalchemy': {'exclude': True}},
        nullable=False,
    )
    _acl = Column(
        MutableList.as_mutable(ACLType),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )

    NODE_LABELS = {
        "estimation": u"Devis",
        "invoice": u"Facture",
        "cancelinvoice": u"Avoir",
        "business": u"Affaire",
        "project": u"Projet",
        "expense_sheet": u"Note de dépenses",
        "workshop": u"Atelier",
        "activity": u"Rendez-vous",
    }
