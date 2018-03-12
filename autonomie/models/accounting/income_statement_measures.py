# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import datetime
import colander
import deform

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
    load_only,
)
from sqlalchemy.sql.expression import func

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)
from autonomie.forms import get_deferred_select
from autonomie.compute.parser import NumericStringParser
from autonomie.models.company import Company
from autonomie.models.accounting.services import (
    IncomeStatementMeasureGridService,
)


logger = logging.getLogger(__name__)


class IncomeStatementMeasureTypeCategory(DBBASE):
    """
    Categories joining the Differente measure types
    """
    __tablename__ = 'income_statement_measure_type_category'
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        "help_msg": u"""Les catégories permettent de regrouper les types
        d'indicateurs afin d'en faciliter la configuration.
        Ils peuvent ensuite être utilisé pour calculer des totaux.<br />
        """
    }
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}}
    )
    label = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Libellé de cette catégorie (seulement visible dans "
                u"l'interface de configuration)",
            }
        },
        nullable=False,
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalchemy': {
            'title': u"Indicateur actif ?", "exclude": True
        }}
    )
    order = Column(
        Integer,
        default=1,
        info={
            'colanderalchemy': {
                'title': u"Ordre au sein de la catégorie",
                "widget": deform.widget.HiddenWidget(),
            }
        }
    )

    attached_types = relationship(
        "IncomeStatementMeasureType",
        back_populates="category",
        cascade='all,delete,delete-orphan',
        info={'colanderalchemy': {'exclude': True}},
    )

    def move_up(self):
        """
        Move the current instance up in the category's order
        """
        order = self.order
        if order > 0:
            new_order = order - 1
            IncomeStatementMeasureTypeCategory.insert(self, new_order)

    def move_down(self):
        """
        Move the current instance down in the category's order
        """
        order = self.order
        new_order = order + 1
        IncomeStatementMeasureTypeCategory.insert(self, new_order)

    @classmethod
    def get_categories(cls, active=True, keys=()):
        """
        :param bool active: Only load active categories
        :param tuple keys: The keys to load (list of str)
        :returns: IncomeStatementMeasureTypeCategory ordered by order key
        :rtype: list
        """
        query = DBSESSION().query(cls)
        if keys:
            query = query.options(load_only(*keys))
        query = query.filter_by(active=active).order_by(cls.order)
        return query.all()

    @classmethod
    def get_by_label(cls, label, active=True):
        """
        :param str label: The label to retrieve
        :param bool active: Only check in active items

        :returns: An IncomeStatementMeasureTypeCategory or None
        :rtype: class or None
        """
        return DBSESSION().query(cls).filter_by(
            active=active
        ).filter_by(label=label).first()

    @classmethod
    def get_next_order(cls):
        """
        :returns: The next available order
        :rtype: int
        """
        query = DBSESSION().query(func.max(cls.order)).filter_by(active=True)
        query = query.first()
        if query is not None and query[0] is not None:
            result = query[0] + 1
        else:
            result = 0
        return result

    @classmethod
    def insert(cls, item, new_order):
        """
        Place the item at the given index

        :param obj item: The item to move
        :param int new_order: The new index of the item
        """
        items = DBSESSION().query(
            cls
        ).filter_by(
            active=True
        ).filter(cls.id != item.id).order_by(cls.order).all()

        items.insert(new_order, item)

        for index, item in enumerate(items):
            item.order = index
            DBSESSION().merge(item)

    @classmethod
    def reorder(cls):
        """
        Regenerate order attributes
        """
        items = cls.get_categories()

        for index, item in enumerate(items):
            item.order = index
            DBSESSION().merge(item)


class IncomeStatementMeasureType(DBBASE):
    """
    IncomeStatement measure type (a limited number of measure types should exist
    """
    __tablename__ = 'income_statement_measure_type'
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        "help_msg": u"""Les indicateurs de comptes résultats permettent de
        regrouper des écritures sous un même libellé.<br />
        Ils permettent d'assembler les comptes de résultats des entrepreneurs.
        <br />Vous pouvez définir ici les préfixes de comptes généraux pour
        indiquer quelles écritures doivent être utilisées pour calculer cet
        indicateur.
        <br />
        Si nécessaire vous pourrez alors recalculer les derniers indicateurs
        générés.
        """
    }
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}}
    )
    category_id = Column(
        ForeignKey(IncomeStatementMeasureTypeCategory.id),
        info={
            'colanderalchemy': {
                "widget": deform.widget.HiddenWidget(),
            }
        },
        default=-1
    )
    label = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Libellé de cet indicateur",
            }
        },
        nullable=False,
    )
    account_prefix = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Rassemble tous les comptes commençant par",
                "description": u"Toutes les écritures dont le compte commence "
                u"par le préfixe fournit seront utilisées pour calculer cet "
                u"indicateur. "
                u"NB : Une liste de préfixe peut être fournie en les "
                u"séparant par des virgules (ex : 42,43), un préfixe peut "
                u"être exclu en plaçant le signe '-' devant (ex: 42,-425 "
                u"incluera tous les comptes 42... sauf les comptes 425...)",
                "missing": colander.required,
            }
        },
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalchemy': {
            'title': u"Indicateur actif ?", "exclude": True
        }}
    )
    order = Column(
        Integer,
        default=1,
        info={
            'colanderalchemy': {
                'title': u"Ordre au sein de la catégorie",
                "widget": deform.widget.HiddenWidget(),
            }
        }
    )
    is_total = Column(
        Boolean(),
        default=False,
        info={'colanderalchemy': {
            "title": u"Cet indicateur correspond-il à un total (il sera mis en "
            u"évidence dans l'interface et ne sera pas utilisé pour le calcul "
            u"des totaux globaux) ?",
        }}
    )
    total_type = Column(
        String(20),
        info={
            "colanderalchemy": {
                "title": u"Type d'indicateurs "
                u"(account_prefix/complex_total/categories)",
                'exclude': True,
            }
        }
    )

    category = relationship(
        "IncomeStatementMeasureTypeCategory",
        info={
            "colanderalchemy": {"exclude": True}
        }
    )
    measures = relationship(
        "IncomeStatementMeasure",
        primaryjoin="IncomeStatementMeasure.measure_type_id"
        "==IncomeStatementMeasureType.id",
        info={
            "colanderalchemy": {"exclude": True}
        }
    )

    @property
    def computed_total(self):
        """
        :returns: True if this type is a computed total (mix of other values)
        :rtype: bool
        """
        return self.is_total and self.total_type in (
            'complex_total', 'categories'
        )

    def match(self, account):
        """
        Check if the current Type definition matches the given account number

        :param str account: A string representing an accounting account (e.g:
            42500000)
        :returns: True or False if it matches
        :rtype: bool
        """
        res = False
        for prefix in self.account_prefix.split(','):
            if not prefix:
                continue
            if prefix.startswith('-'):
                prefix = prefix[1:].strip()
                if account.startswith(prefix):
                    res = False
                    break
            elif not res:
                if account.startswith(prefix):
                    res = True
        return res

    def move_up(self):
        """
        Move the current instance up in the category's order
        """
        order = self.order
        if order > 0:
            new_order = order - 1
            IncomeStatementMeasureType.insert(self, new_order)

    def move_down(self):
        """
        Move the current instance down in the category's order
        """
        order = self.order
        new_order = order + 1
        IncomeStatementMeasureType.insert(self, new_order)

    def compute_total(self, category_totals):
        """
        Compile a total value based on the given category totals

        :param dict category_totals: Totals stored by category labels
        :returns: The compiled total
        :rtype: int
        """
        result = 0
        if self.total_type == 'categories':
            result = self._compute_categories_total(category_totals)
        elif self.total_type == 'complex_total':
            result = self._compute_complex_total(category_totals)
        return result

    def _compute_categories_total(self, all_category_totals):
        """
        Compute the sum of the current's item categories picking them in the
        all_category_totals dict

        :param dict all_category_totals: Totals stored by category labels
        :returns: The compiled total
        :rtype: int
        """
        result = 0
        for category in self.account_prefix.split(','):
            if category in all_category_totals:
                result += all_category_totals[category]
        return result

    def _compute_complex_total(self, all_category_totals):
        """
        Compile the arithmetic operation configure in the current item, using
        datas coming from the all_category_totals dict

        :param dict all_category_totals: Totals stored by category labels
        :returns: The compiled total
        :rtype: int
        """
        result = 0
        try:
            operation = self.account_prefix.format(**all_category_totals)
        except KeyError:
            operation = "0"

        parser = NumericStringParser()
        try:
            result = parser.eval(operation)
        except ZeroDivisionError:
            result = 0
        except Exception:
            logger.exception(u"Error while parsing : %s" % operation)
            result = 0
        return result

    def get_categories(self):
        """
        Return the categories configured in case of a total type

        :rtype: list of IncomeStatementMeasureTypeCategory instances
        """
        category_labels = self.account_prefix.split(',')

        result = []
        for label in category_labels:
            category = IncomeStatementMeasureTypeCategory.get_by_label(label)
            if category is not None:
                result.append(category)
        return result

    def get_categories_labels(self):
        """
        Return the labels of the categories attached to this instance
        :rtype: list
        """
        return [c.label for c in self.get_categories()]

    @classmethod
    def get_by_category(cls, category_id, key=None):
        """
        Collect IncomeStatementMeasureType associated to the given category

        :param int category_id: The id to check for
        :param str key: The key to load (if we want to restrict the query
        :rtype: list
        """
        query = DBSESSION().query(cls)
        if key is not None:
            query = query.options(load_only(key))
        query = query.filter_by(category_id=category_id)
        return query.all()

    @classmethod
    def get_next_order_by_category(cls, category_id):
        """
        :param int category_id: The id of the category to check for
        :returns: The next order available in types from the given category
        :rtype: int
        """
        query = DBSESSION().query(func.max(cls.order)).filter_by(
            category_id=category_id
        ).filter_by(active=True)
        query = query.first()
        if query is not None and query[0] is not None:
            result = query[0] + 1
        else:
            result = 0
        return result

    @classmethod
    def insert(cls, item, new_order):
        """
        Place the item at the given index in the hierarchy of items of the same
        category

        :param obj item: The item to place
        :param int new_order: The index where to place the item
        """
        items = DBSESSION().query(
            cls
        ).filter_by(
            category_id=item.category_id
        ).filter_by(
            active=True
        ).filter(cls.id != item.id).order_by(cls.order).all()

        items.insert(new_order, item)

        for index, item in enumerate(items):
            item.order = index
            DBSESSION().merge(item)

    @classmethod
    def reorder(cls, category_id):
        """
        Regenerate order attributes
        :param int category_id: The category to manage
        """
        items = DBSESSION().query(
            cls
        ).filter_by(
            category_id=category_id
        ).filter_by(active=True).order_by(cls.order).all()

        for index, item in enumerate(items):
            item.order = index
            DBSESSION().merge(item)

    @classmethod
    def get_types(cls, active=True, keys=()):
        query = DBSESSION().query(cls)
        if keys:
            query = query.options(load_only(*keys))
        if active:
            query = query.filter_by(active=True)
        return query

class IncomeStatementMeasureGrid(DBBASE):
    """
    A grid of measures, one grid per month/year couple

    """
    __tablename__ = 'income_statement_measure_grid'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    datetime = Column(
        DateTime(),
        default=datetime.datetime.now,
        info={"colanderalchemy": {'title': u"Heure et date de création"}}
    )
    month = Column(Integer, info={'colanderalchemy': {'title': u"Mois"}})
    year = Column(Integer, info={'colanderalchemy': {'title': u"Année"}})

    company_id = Column(
        ForeignKey('company.id', ondelete="cascade"),
        info={
            "colanderalchemy": {
                'title': u"Entreprise associée à cette opération",
                "widget": get_deferred_select(
                    Company,
                    keys=('id', lambda c: u"%s %s" % (c.name, c.code_compta))
                )
            }
        }
    )
    company = relationship('Company')
    upload_id = Column(
        ForeignKey('accounting_operation_upload.id', ondelete="cascade"),
        info={"colanderalchemy": {'title': u"Related upload"}},
    )
    upload = relationship('AccountingOperationUpload')
    measures = relationship(
        "IncomeStatementMeasure",
        primaryjoin="IncomeStatementMeasureGrid.id=="
        "IncomeStatementMeasure.grid_id",
        cascade="all,delete,delete-orphan",
    )

    _autonomie_service = IncomeStatementMeasureGridService

    def get_company_id(self):
        return self.company_id

    @classmethod
    def get_years(cls, company_id):
        return cls._autonomie_service.get_years(cls, company_id)

    def get_measure_by_type(self, measure_type_id):
        return self._autonomie_service.get_measure_by_type(
            self, measure_type_id
        )


class IncomeStatementMeasure(DBBASE):
    """
    Stores a income_statement measure associated to a given company
    """
    __tablename__ = 'income_statement_measure'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    label = Column(
        String(255),
        info={"colanderalchemy": {'title': u"Libellé"}}
    )
    value = Column(
        Float(precision=2),
        default=0,
        info={"colanderalchemy": {'title': u"Montant"}},
    )
    measure_type_id = Column(
        ForeignKey('income_statement_measure_type.id'),
        info={
            "colanderalchemy": {
                'title': u"Type d'indicateur",
                "widget": get_deferred_select(IncomeStatementMeasureType),
            }
        }
    )
    measure_type = relationship(
        IncomeStatementMeasureType,
        primaryjoin="IncomeStatementMeasureType.id=="
        "IncomeStatementMeasure.measure_type_id",
        info={"colanderalchemy": {'exclude': True}},
    )
    grid_id = Column(ForeignKey('income_statement_measure_grid.id'))

    def __todict__(self, request):
        return {
            "id": self.id,
            "label": self.label,
            "value": self.get_value(),
            "measure_type_id": self.measure_type_id
        }

    def get_value(self):
        return -1 * self.value
