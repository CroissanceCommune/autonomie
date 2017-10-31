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
from autonomie.models.accounting.services import TreasuryMeasureGridService


class TreasuryMeasureType(DBBASE):
    """
    Treasury measure type (a limited number of measure types should exist
    """
    __tablename__ = 'treasury_measure_type'
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        "help_msg": u"""Les indicateurs de trésorerie sont prédéfinis.<br />
        Ils permettent d'assembler les tableaux de bord des entrepreneurs.<br />
        Vous pouvez modifier ici les préfixes de comptes généraux pour indiquer
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
                u"(voir la partie populate pour le détail)"
            }
        },
        default=-1
    )
    label = Column(
        String(255),
        info={
            'colanderalchemy': {
                'exclude': True,
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
                u"indicateur de trésorerie. "
                u"NB : Une liste de préfixe peut être fournie en les \
séparant par des virgules (ex : 42,43)",
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

    def match(self, account):
        res = False
        for prefix in self.account_prefix.split(','):
            if account.startswith(prefix):
                res = True
                break
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


class TreasuryMeasureGrid(DBBASE):
    """
    A grid of measures

    1. Trésorerie du jour : somme des comptes 5 ;
    2. Impôts, taxes et cotisations dues : somme des comptes 42,43 et 44 ;
    3. Fournisseurs à payer : sommes des comptes 40 ;
    4. Trésorerie de référence : somme des trois indicateurs précédents (1,2,3);
    5. Salaires à payer : somme des comptes 425 ;
    6. Notes de dépenses à payer : somme des comptes 421 ;
    7. Clients à encaisser : somme des 41 ;
    8. Trésorerie future : somme de la trésorerie de référence et des trois
    indicateurs précédents (5,6,7) ;
    9. Liste des entrées pour les comptes 1xxxxx,2xxxxx et 3xxxxx.
    """
    __tablename__ = 'treasury_measure_grid'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    datetime = Column(
        DateTime(),
        default=datetime.datetime.now,
        info={"colanderalchemy": {'title': u"Heure et date de création"}}
    )
    date = Column(
        Date(),
        info={"colanderalchemy": {'title': u"Date du dépôt"}}
    )
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
        "TreasuryMeasure",
        primaryjoin="TreasuryMeasureGrid.id==TreasuryMeasure.grid_id",
        cascade="all,delete,delete-orphan",
    )

    _autonomie_service = TreasuryMeasureGridService

    @classmethod
    def last(cls, company_id):
        return cls._autonomie_service.last(cls, company_id)

    def __todict__(self, request):
        """
        Compile the different measures and return a dict representation of
        the grid
        """
        result = {"date": self.date, "id": self.id, "upload_id": self.upload_id}
        result["measures"] = measures_dict = {}

        for measure in self.measures:
            m_list = measures_dict.setdefault(
                measure.measure_type.internal_id, []
            )
            m_list.append(measure.__todict__(request))

        ref_treasury = 0
        for i in range(1, 4):
            if i in measures_dict:
                ref_treasury += measures_dict[i][0]['value']

        measures_dict[4] = [{
            "label": u"Trésorerie de référence",
            "value": ref_treasury
        }]

        for i in range(5, 8):
            if i in measures_dict:
                ref_treasury += measures_dict[i][0]['value']

        measures_dict[8] = [{
            "label": u"Trésorerie future",
            "value": ref_treasury,
        }]
        return result

    @classmethod
    def get_years(cls):
        return cls._autonomie_service.get_years(cls)

    def get_first_measure(self):
        return self._autonomie_service.measure_by_internal_id(self, 1)

    def get_company_id(self):
        return self.company_id


class TreasuryMeasure(DBBASE):
    """
    Stores a treasury measure associated to a given company
    """
    __tablename__ = 'treasury_measure'
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
        ForeignKey('treasury_measure_type.id'),
        info={
            "colanderalchemy": {
                'title': u"Type d'indicateur",
                "widget": get_deferred_select(TreasuryMeasureType),
            }
        }
    )
    measure_type = relationship(
        TreasuryMeasureType,
        primaryjoin="TreasuryMeasureType.id==TreasuryMeasure.measure_type_id",
        info={"colanderalchemy": {'exclude': True}},
    )
    grid_id = Column(ForeignKey('treasury_measure_grid.id'))

    def __todict__(self, request):
        return {
            "id": self.id,
            "label": self.label,
            "value": self.value,
            "measure_type_id": self.measure_type_id
        }
