#-*-coding:utf-8-*-
"""1.5 : Moving manualinvoice as task with polymorphism

Revision ID: 2a7a5275c441
Revises: 41116dd5c5c8
Create Date: 2012-11-12 13:56:59.664834

"""

# revision identifiers, used by Alembic.
revision = '2a7a5275c441'
down_revision = '41116dd5c5c8'

from autonomie.alembic.utils import force_rename_table
from autonomie.alembic.utils import table_exists
from autonomie.models.task.invoice import ManualInvoice


import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import BigInteger
from sqlalchemy import DateTime
from autonomie.models import DBBASE
from autonomie.models.task.invoice import Payment

def upgrade():
    # Fix an error in table names for some installations
    class OldManualInvoice(DBBASE):
        """
            Modèle pour les factures manuelles (ancienne version)
        """
        __tablename__ = 'manualinvoice'
        id = Column('id', BigInteger, primary_key=True)
        officialNumber = Column('sequence_id', BigInteger)
        description = Column('libelle', String(255))
        montant_ht = Column("montant_ht", Integer)
        tva = Column("tva", Integer)
        payment_ok = Column("paiement_ok", Integer)
        statusDate = Column("paiement_date", Date())
        paymentMode = Column("paiement_comment", String(255))
        taskDate = Column("date_emission", Date(),
                                    default=datetime.datetime.now)
        created_at = Column("created_at", DateTime,
                                        default=datetime.datetime.now)
        updated_at = Column("updated_at", DateTime,
                                        default=datetime.datetime.now,
                                        onupdate=datetime.datetime.now)
        client_id = Column('client_id', Integer,
                                ForeignKey('customer.code'))

        company_id = Column('compagnie_id', Integer,
                                ForeignKey('company.id'))


    if not table_exists("manualinvoice"):
        force_rename_table('manual_invoice', 'manualinvoice')
    from autonomie.models import DBSESSION
    for manualinv in OldManualInvoice.query().all():
        m = ManualInvoice()
        m.montant_ht = manualinv.montant_ht
        m.tva = manualinv.tva
        m.client_id = manualinv.client_id
        m.company_id = manualinv.company_id
        m.description = manualinv.description
        m.CAEStatus = 'valid'
        if manualinv.payment_ok == '1' or manualinv.montant_ht < 0:
            m.CAEStatus = "resulted"
        if manualinv.montant_ht < 0:
            if manualinv.paymentMode == u"chèque":
                payment_mode = "CHEQUE"
            elif manualinv.paymentMode == u"virement":
                payment_mode = "VIREMENT"
            else:
                payment_mode = None
            if payment_mode:
                # We don't care about amounts since there is only one payment
                payment = Payment(mode=payment_mode, date=manualinv.statusDate,
                                amount=0)
                m.payments.append(payment)
        m.statusDate = manualinv.statusDate
        m.taskDate = manualinv.taskDate
        m.creationDate = manualinv.created_at
        m.updateDate = manualinv.updated_at
        m.phase_id = 0
        m.name = u"Facture manuelle %s" % manualinv.officialNumber
        m.officialNumber = manualinv.officialNumber
        m.owner_id = 0
        DBSESSION.add(m)


def downgrade():
    pass
