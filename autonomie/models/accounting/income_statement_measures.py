# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Date,
    Boolean,
)
from sqlalchemy.orm import relationship

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)
from autonomie.forms import get_deferred_select
from autonomie.models.company import Company
from autonomie.models.accounting.services import GeneralLedgerMeasureGridService


CATEGORIES = [
    "Produits",
    "Achats",
    "Charges",
    "Salaire Brut",
]
CATEGORY_NUMBERS = tuple(range(len(CATEGORIES)))  # 0,1,2,3,4


class GeneralLedgerMeasureType(DBBASE):
    """
    GeneralLedger measure type (a limited number of measure types should exist
    """
    __tablename__ = 'general_ledger_measure_type'
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        "help_msg": u"""Les indicateurs de comptes résultats permettent de
        regrouper Charges, Produits ou Achats sous un même libellé.<br />
        Ils permettent d'assembler les comptes de résultatsdes entrepreneurs.<br />
        Vous pouvez définir ici les préfixes de comptes généraux pour indiquer
        quelles écritures doivent être utilisées pour calculer cet indicateur.
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
    internal_id = Column(
        Integer,
        info={
            'colanderalchemy': {
                'exclude': True,
                'title': u"Identifiant utilisé en interne pour le regroupement "
                u"par catégorie"
                u"(voir ci-dessus pour le détail)",
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
        }
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
                "exclude": True,
            }
        }
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
            if prefix.startswith('-'):
                prefix = prefix[1:].strip()
                if account.startswith(prefix):
                    res = False
                    break
            elif not res:
                if account.startswith(prefix):
                    res = True
        return res

    @classmethod
    def get_by_internal_id(cls, internal_id):
        query = DBSESSION().query(cls.id).filter_by(internal_id=internal_id)
        query = query.first()

        if query is not None:
            result = query[0]
        else:
            result = None
        return result


class GeneralLedgerMeasureGrid(DBBASE):
    """
    A grid of measures, one grid per month/year couple

    """
    __tablename__ = 'general_ledger_measure_grid'
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
        "GeneralLedgerMeasure",
        primaryjoin="GeneralLedgerMeasureGrid.id==GeneralLedgerMeasure.grid_id",
        cascade="all,delete,delete-orphan",
    )

    _autonomie_service = GeneralLedgerMeasureGridService

    def get_company_id(self):
        return self.company_id


class GeneralLedgerMeasure(DBBASE):
    """
    Stores a general_ledger measure associated to a given company
    """
    __tablename__ = 'general_ledger_measure'
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
        ForeignKey('general_ledger_measure_type.id'),
        info={
            "colanderalchemy": {
                'title': u"Type d'indicateur",
                "widget": get_deferred_select(GeneralLedgerMeasureType),
            }
        }
    )
    measure_type = relationship(
        GeneralLedgerMeasureType,
        primaryjoin="GeneralLedgerMeasureType.id==GeneralLedgerMeasure.measure_type_id",
        info={"colanderalchemy": {'exclude': True}},
    )
    grid_id = Column(ForeignKey('general_ledger_measure_grid.id'))

    def __todict__(self, request):
        return {
            "id": self.id,
            "label": self.label,
            "value": self.value,
            "measure_type_id": self.measure_type_id
        }
