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
)
from sqlalchemy.orm import relationship

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.forms import get_deferred_select
from autonomie.models.company import Company


class AccountingOperationUpload(DBBASE):
    """
    Represent a newly parsed file
    """
    __tablename__ = 'accounting_operation_upload'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(),
        default=datetime.datetime.now,
        info={"colanderalchemy": {'title': u"Heure et date de création"}}
    )
    filename = Column(
        String(100),
        info={"colanderalchemy": {'title': u"Nom du fichier"}}
    )
    operations = relationship(
        "AccountingOperation",
        primaryjoin="AccountingOperation.upload_id"
        "==AccountingOperationUpload.id",
        order_by="AccountingOperation.analytical_account",
        cascade='all,delete,delete-orphan',
    )
    date = Column(
        Date(),
        info={
            "colanderalchemy": {
                'title': u"Date à associer aux données de ce fichier "
                u"(extraite du nom du fichier)"
            }
        }
    )
    md5sum = Column(
        String(34),
        info={
            "colanderalchemy": {
                "title": u"Somme md5 du fichier",
                "description": u"Permet d'identifier les fichiers déjà traités",
            }
        }
    )


class AccountingOperation(DBBASE):
    __tablename__ = 'accounting_operation'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    datetime = Column(
        DateTime(),
        default=datetime.datetime.now,
        info={"colanderalchemy": {'title': u"Heure et date de création"}}
    )
    analytical_account = Column(
        String(20),
        info={
            'colanderalchemy': {'title': u"Compte analytique de l'entreprise"}
        }
    )
    general_account = Column(
        String(20),
        info={
            'colanderalchemy': {'title': u"Compte analytique de l'entreprise"}
        }
    )
    label = Column(
        String(80),
        info={'colanderalchemy': {'title': u"Libellé"}},
    )
    debit = Column(
        Float(precision=2),
        info={'colanderalchemy': {'title': u"Débit"}},
    )
    credit = Column(
        Float(precision=2),
        info={'colanderalchemy': {'title': u"Crédit"}},
    )
    balance = Column(
        Float(precision=2),
        info={'colanderalchemy': {'title': u"Solde"}},
    )
    company_id = Column(
        ForeignKey('company.id', ondelete="CASCADE"),
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
    company = relationship(
        'Company',
        info={"colanderalchemy": {'exclude': True}},
    )
    upload_id = Column(
        ForeignKey('accounting_operation_upload.id', ondelete="CASCADE")
    )

    def __json__(self, request):
        return dict(
            analytical_account=self.analytical_account,
            general_account=self.general_account,
            label=self.label,
            debit=self.debit,
            credit=self.credit,
            balance=self.balance,
            company_id=self.company_id,
        )
