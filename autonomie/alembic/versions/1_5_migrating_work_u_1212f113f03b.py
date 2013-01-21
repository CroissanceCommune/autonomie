"""1.5 : Migrating work unity

Revision ID: 1212f113f03b
Revises: 1f07ae132ac8
Create Date: 2013-01-21 11:53:56.598914

"""

# revision identifiers, used by Alembic.
revision = '1212f113f03b'
down_revision = '1f07ae132ac8'

from alembic import op
import sqlalchemy as sa

from autonomie.models import DBSESSION
from autonomie.models.task import WorkUnit
from autonomie.models.task.estimation import EstimationLine
from autonomie.models.task.invoice import InvoiceLine
from autonomie.models.task.invoice import CancelInvoiceLine

UNITIES = dict(NONE="",
               HOUR=u"heure(s)",
               DAY=u"jour(s)",
               WEEK=u"semaine(s)",
               MONTH=u"mois",
               FEUIL=u"feuillet(s)",
               PACK=u"forfait")

UNITS = (u"heure(s)",
         u"jour(s)", u"semaine(s)", u"mois", u"forfait", u"feuillet(s)",)

def translate_unity(unity):
    return UNITIES.get(unity, UNITIES["NONE"])

def translate_inverse(unity):
    for key, value in UNITIES.items():
        if unity == value:
            return key
    else:
        return u"NONE"

def upgrade():
    # Adding some characters to the Lines
    for table in "estimation_line", "invoice_line", "cancelinvoice_line":
        op.alter_column(table, "unity", type_=sa.String(100))

    for value in UNITS:
        unit = WorkUnit(label=value)
        DBSESSION().add(unit)
    for factory in (EstimationLine, InvoiceLine, CancelInvoiceLine):
        for line in factory.query():
            line.unity = translate_unity(line.unity)
            DBSESSION().merge(line)

def downgrade():
    for factory in (EstimationLine, InvoiceLine, CancelInvoiceLine):
        for line in factory.query():
            line.unity = translate_inverse(line.unity)
            DBSESSION().merge(line)
    for value in WorkUnit.query():
        DBSESSION().delete(value)
