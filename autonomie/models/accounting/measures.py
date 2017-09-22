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
    id = Column(Integer, primary_key=True)
    label = Column(
        String(255),
        info={
            'colanderalachemy': {'title': u"Libellé de cet indicateur"}
        }
    )
    account_start_prefix = Column(
        String(10),
        info={
            'colanderalachemy': {'title': u"Depuis les comptes commençant par"}
        },
    )
    account_end_prefix = Column(
        String(10),
        info={
            'colanderalachemy': {'title': u"Jusqu'au comptes commençant par"}
        },
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalachemy': {'title': u"Indicateur actif ?"}}
    )


class TreasuryMeasure(DBBASE):
    """
    Stores a treasury measure associated to a given company
    """
    __tablename__ = 'treasury_measure'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    datetime = Column(
        DateTime(),
        default=datetime.datetime.now,
        info={"colanderalchemy": {'title': u"Heure et date de création"}}
    )
    label = Column(
        String(255),
        info={"colanderalchemy": {'title': u"Libellé"}}
    )
    value = Column(
        Float(precision=2),
        info={"colanderalchemy": {'title': u"Montant"}}
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
    company_id = Column(
        ForeignKey('company.id'),
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
