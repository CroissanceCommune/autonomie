"""
    form schemas for invoices related views
"""
from datetime import date
import colander

from autonomie.views.forms.lists import BaseListsSchema


STATUS_OPTIONS = ((u"Toutes les factures", "both"),
                  (u"Les factures payées", "paid"),
                  (u"Seulement les impayés", "notpaid"))

@colander.deferred
def default_year(node, kw):
    return date.today().year

class InvoicesListSchema(BaseListsSchema):
    # We override the search param, it needs to be an integer in our case
    # (officialNumber)
    search = colander.SchemaNode(colander.Integer(), missing=None)
    status = colander.SchemaNode(colander.String(),
            validator=colander.OneOf([s[1] for s in STATUS_OPTIONS]),
            missing='both')
    year = colander.SchemaNode(colander.Integer(), missing=default_year)
    client_id = colander.SchemaNode(colander.Integer(), missing=-1)
    company_id = colander.SchemaNode(colander.Integer(), missing=-1)