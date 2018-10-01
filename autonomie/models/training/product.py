# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * BODRERO Sébastien <bodrero.sebastien@gmail.com>
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
    Training product model : represents trainings product
"""

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Boolean,
    Integer,
    Table,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from autonomie import forms
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.models.sale_product import SaleProductGroup
from autonomie.models.sale_product import SaleProductCategory
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)
from autonomie.models.tools import get_excluded_colanderalchemy

TRAINING_TYPE_TO_TRAINING_GROUP_REL_TABLE = Table(
    "training_type_sale_training_group_rel",
    DBBASE.metadata,
    Column(
        "training_type_id",
        Integer,
        ForeignKey('training_type_options.id', ondelete='cascade')
    ),
    Column(
        "sale_training_group_id",
        Integer,
        ForeignKey(
            'sale_training_group.id',
            ondelete='cascade',
            name="fk_training_type_sale_training_group_rel_id"
        )
    ),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


class TrainingTypeOptions(ConfigurableOption):
    """
    Different type of training
    """
    __colanderalchemy_config__ = {
        'title': u"Type de formation",
        'validation_msg': u"Les types de formation ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class SaleTrainingGroup(SaleProductGroup):
    """
    A product group model
    :param id: unique id
    :param goals: goals of title of the training item
    :param prerequisites: prerequisites to subscribe to the training session
    :param for_who: target of the training item
    :param duration: duration of the training item
    :param content: content of the training item
    :param teaching_method: teaching_method used in training session
    :param logistics_means: logistics_means implemented for the training session
    :param more_stuff: Les plus...
    :param evaluation: evaluation criteria
    :param place: place if the training session
    :param modality: modality of the training session
    :param types: types of the training
    :param date: date og the training session
    :param price: price of the training session
    :param free_1: free input
    :param free_2: free input
    :param free_3: free input
    :param company_id: company that owns the training
    :param company_id: company that owns the group
    """
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'training'}
    id = Column(ForeignKey('sale_product_group.id'), primary_key=True)

    goals = Column(
        String(255),
        default='',
    )

    prerequisites = Column(
        String(255),
        default=''
    )

    for_who = Column(
        String(255),
        default=''
    )

    duration = Column(
        String(255),
        nullable=False,
        default=''
    )

    content = Column(
        String(255),
        default=''
    )

    teaching_method = Column(
        String(255),
        default=''
    )

    logistics_means = Column(
        String(255),
        default=''
    )

    more_stuff = Column(
        String(255),
        default=''
    )

    evaluation = Column(
        String(255),
        default=''
    )

    place = Column(
        String(255),
        default=''
    )

    modalityOne = Column(
        Boolean(),
        default=False
    )

    modalityTwo = Column(
        Boolean(),
        default=False
    )

    types = relationship(
        'TrainingTypeOptions',
        secondary=TRAINING_TYPE_TO_TRAINING_GROUP_REL_TABLE,
        info={
            'export': {'related_key': 'label'},
            'children': forms.get_sequence_child_item(TrainingTypeOptions),
        },
    )

    date = Column(
        String(255),
        default=''
    )

    price = Column(
        String(255),
        default=''
    )

    free_1 = Column(
        String(255),
        default=''
    )

    free_2 = Column(
        String(255),
        default=''
    )

    free_3 = Column(
        String(255),
        default=''
    )

    category = relationship(
        SaleProductCategory,
        backref=backref('training_groups'),
        info={'colanderalchemy': forms.EXCLUDED},
    )

    def __json__(self, request):
        """
        Json repr of our model
        """
        return dict(
            id=self.id,
            label=self.label,
            ref=self.ref,
            title=self.title,
            description=self.description,
            products=[product.__json__(request) for product in self.products],
            category_id=self.category_id,
            goals=self.goals,
            prerequisites=self.prerequisites,
            for_who=self.for_who,
            duration=self.duration,
            content=self.content,
            teaching_method=self.teaching_method,
            logistics_means=self.logistics_means,
            more_stuff=self.more_stuff,
            evaluation=self.evaluation,
            place=self.place,
            modalityOne=self.modalityOne,
            modalityTwo=self.modalityTwo,
            types=[type.__json__(request) for type in self.types],
            date=self.date,
            price=self.price,
            free_1=self.free_1,
            free_2=self.free_2,
            free_3=self.free_3,
        )

    @property
    def company(self):
        return self.category.company