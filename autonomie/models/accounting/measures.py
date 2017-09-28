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
)
from autonomie.forms import get_deferred_select
from autonomie.models.company import Company


class TreasuryMeasureType(DBBASE):
    """
    Treasury measure type (a limited number of measure types should exist
    """
    __tablename__ = 'treasury_measure_type'
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        "help_msg": u"""Les indicateurs décrits ici sont prédéfinis.
        Ils permettent d'assembler les tableaux de bord des entrepreneurs.
        Vous pouvez modifier ici les préfixes de comptes généraux pour indiquer
        quelles écritures doivent être utilisées pour les calculer."""
    }
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalachemy': {'exclude': True}}
    )
    internal_id = Column(
        Integer,
        info={'colanderalachemy': {'exclude': True}},
        default=-1
    )
    label = Column(
        String(255),
        info={
            'colanderalachemy': {'title': u"Libellé de cet indicateur"}
        }
    )
    account_prefix = Column(
        String(10),
        info={
            'colanderalachemy': {
                'title': u"Depuis les comptes commençant par",
                "description": u"Une liste de préfixe peut être fournie en les \
séparant par des virgules (ex : 42,43)",
            }
        },
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalachemy': {'title': u"Indicateur actif ?"}}
    )

    def match(self, account):
        res = False
        for prefix in self.account_prefix.split(','):
            if account.startswith(prefix):
                res = True
                break
        return res


class TreasuryMeasureGrid(DBBASE):
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
        info={"colanderalachemy": {'title': u"Related upload"}},
    )
    upload = relationship('AccountingOperationUpload')
    measures = relationship(
        "TreasuryMeasure",
        primaryjoin="TreasuryMeasureGrid.id==TreasuryMeasure.grid_id",
        cascade="all,delete,delete-orphan",
    )


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
