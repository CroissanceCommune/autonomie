# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import colander

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
)

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie import forms

logger = logging.getLogger(__name__)


class ExpenseType(DBBASE):
    """
        Base Type for expenses
        :param label: Label of the expense type that will be used in the UI
        :param code: Analytic code related to this expense
        :param type: Column for polymorphic discrimination
    """
    __colanderalchemy_config__ = {
        'title': u"Configuration des types de dépenses",
        'validation_msg': u"Les types de dépenses ont bien été configurés",
        "help_msg": u"Configurer les types de dépenses utilisables dans \
les formulaires de saisie",
    }
    __tablename__ = 'expense_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_on="type",
                           polymorphic_identity="expense",
                           with_polymorphic='*')
    id = Column(
        Integer,
        primary_key=True,
    )
    type = Column(
        String(30),
        nullable=False,
    )
    active = Column(
        Boolean(),
        default=True,
    )
    label = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Libellé",
            }
        },
        nullable=False,
    )
    code = Column(
        String(15),
        info={
            'colanderalchemy': {
                'title': u"Compte de charge de la dépense",
            }
        },
        nullable=False,
    )

    code_tva = Column(
        String(15),
        default="",
        info={
            'colanderalchemy': {
                'title': u"Code TVA (si nécessaire)",
            }
        }
    )
    compte_tva = Column(
        String(15),
        default="",
        info={
            'colanderalchemy': {
                'title': u"Compte de TVA déductible (si nécessaire)",
            }
        }
    )
    contribution = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Inclue dans la contribution ?",
                'description': u"Ce type de dépense est-il intégré dans la \
contribution à la CAE ?"
            }
        }
    )

    def __json__(self, request=None):
        return {
            "id": self.id,
            "value": self.id,
            "active": self.active,
            "code": self.code,
            "label": self.display_label,
        }

    @property
    def display_label(self):
        return u"{0} ({1})".format(self.label, self.code)


class ExpenseKmType(ExpenseType):
    """
        Type of expenses related to kilometric fees
    """
    __colanderalchemy_config__ = {
        'title': u"type de dépenses kilométriques",
        'validation_msg': u"Les types de dépenses kilométriques ont bien été \
configurés",
        "help_msg": u"Configurer les types de dépenses kilométriques \
utilisables dans les notes de dépense",
    }
    __tablename__ = 'expensekm_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensekm')
    id = Column(
        Integer,
        ForeignKey('expense_type.id'),
        primary_key=True,
    )
    amount = Column(
        Float(precision=4),
        info={
            'colanderalchemy': {
                'title': u"Tarif au km",
            }
        },
        nullable=False,
    )
    year = Column(
        Integer,
        nullable=True,
        info={
            "colanderalchemy": {
                "title": u"Année de référence",
                "description": u"Année à laquelle ce barême est associé",
            }
        }
    )

    def __json__(self, request=None):
        res = ExpenseType.__json__(self)
        res['amount'] = self.amount
        return res

    def duplicate(self, year):
        new_model = ExpenseKmType()
        new_model.amount = self.amount
        new_model.year = year
        new_model.label = self.label
        new_model.code = self.code
        new_model.code_tva = self.code_tva
        new_model.compte_tva = self.compte_tva
        new_model.contribution = self.contribution
        return new_model

    def get_by_year(self, year):
        """
        Retrieving the ExpenseKmType matching the current one but for the given
        year

        :param int year: The year the type should be attached to
        :returns: A ExpenseKmType instance
        """
        if year == self.year:
            return self
        else:
            query = ExpenseKmType.query().filter_by(year=year)
            query = query.filter_by(label=self.label)
            query = query.filter_by(code=self.code)
            return query.first()


class ExpenseTelType(ExpenseType):
    """
        Type of expenses related to telefonic fees
    """
    __colanderalchemy_config__ = {
        'title': u"type de dépenses téléphoniques",
        'validation_msg': u"Les types de dépenses téléphoniques ont bien été \
configurés",
        "help_msg": u"Configurer les types de dépenses téléphoniques \
utilisables dans les notes de dépense",
    }
    __tablename__ = 'expensetel_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensetel')
    id = Column(
        Integer,
        ForeignKey('expense_type.id'),
        primary_key=True,
    )
    percentage = Column(
        Integer,
        nullable=False,
    )
    initialize = Column(
        Boolean,
        default=True,
        info={
            'colanderalchemy': {
                'title': u"Créer une entrée par défaut ?",
                'description': u"Dans le formulaire de saisie des notes de \
dépense, une ligne sera automatiquement ajouté au Frais de l'entrepreneur."
            }
        }
    )

    def __json__(self, request=None):
        res = ExpenseType.__json__(self)
        res['percentage'] = self.percentage
        return res
