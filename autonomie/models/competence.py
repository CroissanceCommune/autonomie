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
import datetime
import deform

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    Float,
    Date,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.forms import (
    EXCLUDED,
    get_deferred_select,
    get_hidden_field_conf,
)

from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)


EPSILON = 0.01


class CompetenceDeadline(ConfigurableOption):
    __colanderalchemy_config__ = {
        'title': u"Échéances d'évaluation",
        'validation_msg': u"Les échéances ont bien été configurées",
        "help_msg": u"Configurer les échéances à laquelle les compétences des \
entrepreneurs seront évaluées",
        "seq_widget_options": {
            'add_subitem_text_template': u"Ajouter une échéance",
        }
    }
    id = get_id_foreignkey_col('configurable_option.id')

    def __json__(self, request):
        return dict(
            id=self.id,
            label=self.label,
        )

    @classmethod
    def query(cls, *args):
        query = super(CompetenceDeadline, cls).query(*args)
        return query


class CompetenceScale(ConfigurableOption):
    __colanderalchemy_config__ = {
        "title": u"Barêmes",
        'validation_msg': u"Les barêmes ont bien été configurés",
        "help_msg": u"Configurer les échelles d'évaluation des compétences. \
<br />Dans la grille de compétence, chaque valeur correspondra à une colonne.",
        "seq_widget_options": {
            'add_subitem_text_template': u"Ajouter un niveau à l'échelle "
            u"d'évaluation",
        }
    }
    id = get_id_foreignkey_col('configurable_option.id')
    value = Column(
        Float(),
        info={
            'colanderalchemy': {
                'title': u"Valeur numérique",
                'description': u"Valeurs utilisées comme unité dans \
les graphiques",
            }
        }
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            value=self.value,
            label=self.label,
        )

    @classmethod
    def query(cls, *args):
        query = super(CompetenceScale, cls).query(*args)
        query = query.order_by(CompetenceScale.value)
        return query


class CompetenceOption(ConfigurableOption):
    """
    A competence model (both for the main one and the sub-competences)

    :param int required_id: The id of the bareme element needed
    """
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        "title": u"Grille de compétences",
        "seq_widget_options": {
            "add_subitem_text_template": u"Ajouter une compétence",
        },
        "validation_msg": u"La grille de compétences a bien été configurée",
        "help_msg": u"Définissez des compétences, celles-ci sont \
composées: <ul><li>D'un libellé</li>\
<li>D'un ensemble de sous-compétences</li></ul>"
    }
    id = get_id_foreignkey_col('configurable_option.id')
    # To be removed in 3.2
    requirement = Column(
        Float(),
        default=0,
        info={'colanderalchemy': {"exclude": True}}
    )
    children = relationship(
        "CompetenceSubOption",
        primaryjoin="CompetenceOption.id==CompetenceSubOption.parent_id",
        info={
            'colanderalchemy': {
                'title': u"Sous-compétences associées",
                "widget": deform.widget.SequenceWidget(
                    add_subitem_text_template=u"Ajouter une \
sous-compétence",
                    min_len=1,
                )
            },
        },
        back_populates='parent',
    )

    @classmethod
    def query(cls, active=True, *args):
        query = super(CompetenceOption, cls).query(*args)
        query = query.filter_by(active=active)
        return query

    def __json__(self, request):
        return dict(
            id=self.id,
            label=self.label,
            requirements=[req.__json__(request) for req in self.requirement],
            children=[child.__json__(request) for child in self.children],
        )

    @classmethod
    def __radar_datas__(cls, deadline_id):
        result = []
        for option in cls.query():
            result.append(
                {
                    'axis': option.label,
                    'value': option.get_requirement(deadline_id)
                }
            )
        return result

    def get_requirement(self, deadline_id):
        for req in self.requirements:
            if req.deadline_id == deadline_id:
                return req.requirement
        return 0


class CompetenceSubOption(ConfigurableOption):
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {"title": u"Sous-compétence"}
    id = get_id_foreignkey_col('configurable_option.id')
    parent_id = Column(
        ForeignKey("competence_option.id"),
        info={
            'colanderalchemy': EXCLUDED
        }
    )
    parent = relationship(
        "CompetenceOption",
        primaryjoin="CompetenceOption.id==CompetenceSubOption.parent_id",
        cascade="all",
        info={
            'colanderalchemy': EXCLUDED
        },
        back_populates='children',
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            label=self.label,
            parent_id=self.parent_id,
        )


class CompetenceRequirement(DBBASE):
    __colanderalchemy_config__ = {
        "title": u"Niveau de référence de la grille de compétence",
        "validation_msg": u"Les niveaux de référence de la grille de \
compétences ont bien été configurés",
        "help_msg": u"Pour chaque compétence, définissez les niveaux de \
référence à chaque échéance.",
        "seq_widget_options": {
            "add_subitem_text_template": u"Ajouter un niveau de référence",
        },
    }
    competence_id = Column(
        ForeignKey('competence_option.id'),
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()},
    )
    deadline_id = Column(
        ForeignKey('competence_deadline.id'), primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()},
    )
    requirement = Column(
        Float(),
        default=0,
        info={
            'colanderalchemy': {
                "title": u"Niveau de référence",
                "widget": get_deferred_select(
                    CompetenceScale,
                    mandatory=True,
                    keys=('value', 'label'),
                )
            }
        }
    )

    competence = relationship(
        'CompetenceOption',
        backref=backref(
            'requirements',
            info={
                'colanderalchemy': {
                    "title": u"Niveaux de référence pour cette compétence",
                },
            }
        ),
        info={
            'colanderalchemy': {"exclude": True},
        }
    )
    deadline = relationship(
        "CompetenceDeadline",
        backref=backref(
            'requirements',
            info={
                'colanderalchemy': {"exclude": True},
            }
        ),
        info={
            'colanderalchemy': {"exclude": True},
        }
    )

    def __json__(self, request):
        return dict(
            deadline_id=self.deadline_id,
            competence_id=self.competence_id,
            reqirement=self.requirement,
            deadline_label=self.deadline.label,
        )


class CompetenceGrid(DBBASE):
    """
    The competences grid
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)

    deadline_id = Column(ForeignKey("competence_deadline.id"))
    deadline = relationship("CompetenceDeadline")
    created_at = Column(
        Date(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Créé(e) le",
            }
        },
        default=datetime.date.today,
    )

    updated_at = Column(
        Date(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Mis(e) à jour le",
            }
        },
        default=datetime.date.today,
        onupdate=datetime.date.today
    )

    contractor_id = Column(ForeignKey("accounts.id"))
    contractor = relationship(
        "User",
        backref=backref(
            "competence_grids",
            info={'colanderalchemy': EXCLUDED, 'export': EXCLUDED},
        ),
    )

    def ensure_item(self, competence_option):
        """
        Return the item that is used to register evaluation for the given
        competence_option

        :param obj competence_option: The competence_option object
        """
        query = CompetenceGridItem.query()
        query = query.filter_by(
            option_id=competence_option.id,
            grid_id=self.id,
        )
        item = query.first()
        if item is None:
            item = CompetenceGridItem(option_id=competence_option.id)
            self.items.append(item)
        for suboption in competence_option.children:
            item.ensure_subitem(suboption)

        return item

    def __json__(self, request):
        return dict(
            id=self.id,
            deadline_id=self.deadline_id,
            contractor_id=self.contractor_id,
            deadline_label=self.deadline.label,
            items=[item.__json__(request) for item in self.items]
        )

    def __radar_datas__(self):
        return [item.__radar_datas__() for item in self.items]


class CompetenceGridItem(DBBASE):
    """
    An item of the grid compound of two text boxes

    represented by a table
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)

    progress = Column(Text(), default='')

    option_id = Column(ForeignKey("competence_option.id"))
    option = relationship(
        "CompetenceOption",
        primaryjoin="and_(CompetenceOption.id==CompetenceGridItem.option_id, "
        "CompetenceOption.active==True)"
    )

    grid_id = Column(ForeignKey("competence_grid.id"))
    grid = relationship(
        "CompetenceGrid",
        backref=backref(
            "items"
        ),
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            progress=self.progress,
            option_id=self.option_id,
            label=self.option.label,
            requirement=self.option.get_requirement(self.grid.deadline_id),
            grid_id=self.grid_id,
            subitems=[subitem.__json__(request) for subitem in self.subitems],
            average=self.average,
        )

    @property
    def average(self):
        """
        Return the average evaluation for this item
        """
        values = [subitem.evaluation for subitem in self.subitems
                  if subitem.evaluation is not None]
        if not values:
            values = [0.0]
        sum_of_values = sum(values)
        return sum_of_values / float(len(self.subitems))

    def ensure_subitem(self, competence_option):
        """
        Return a sub competence item used for the evaluation of the give
        competence option

        :param obj competence_option: The competence_option object
        """
        query = CompetenceGridSubItem.query()
        query = query.filter_by(
            option_id=competence_option.id,
            item_id=self.id,
        )
        item = query.first()
        if item is None:
            self.subitems.append(
                CompetenceGridSubItem(
                    option_id=competence_option.id,
                    item_id=self.id,
                )
            )
        return item

    def __radar_datas__(self):
        return {'axis': self.option.label, 'value': self.average}

    @property
    def contractor(self):
        return self.grid.contractor


class CompetenceGridSubItem(DBBASE):
    """
    A subcompetence represented by a table line
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)

    evaluation = Column(Float(), default=None)

    option_id = Column(ForeignKey("competence_sub_option.id"))
    option = relationship("CompetenceSubOption")

    comments = Column(Text(), default='')

    item_id = Column(ForeignKey("competence_grid_item.id"))
    item = relationship(
        "CompetenceGridItem",
        backref=backref(
            "subitems"
        ),
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            evaluation=self.evaluation,
            option_id=self.option_id,
            label=self.option.label,
            item_id=self.item_id,
            comments=self.comments,
        )

    @property
    def scale(self):
        """
        Returns the scale matching the current evaluation value Since scales can
        be changed, we get the first scale that is <= evaluation
        """
        scales = CompetenceScale.query()
        if self.evaluation is None:
            result = scales.first()
        else:
            result = scales.filter(
                CompetenceScale.value <= self.evaluation + EPSILON
            ).order_by(CompetenceScale.value).all()[-1]
        if result is None:  # No scale is lower than evaluation
            result = scales.first()
        return result

    @property
    def contractor(self):
        return self.item.grid.contractor
