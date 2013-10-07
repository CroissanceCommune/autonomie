"""
    Client handling forms schemas
"""
import colander
import logging

from deform import widget

from autonomie.models.client import Client
from autonomie.views.forms.widgets import get_mail_input
from autonomie.views.forms.lists import BaseListsSchema

log = logging.getLogger(__name__)

def get_client_from_request(request):
    if request.context.__name__ == 'client':
        return request.context
    else:
        return None

def get_company_id_from_request(request):
    if request.context.__name__ =='company':
        return request.context.id
    elif request.context.__name__ == 'client':
        return request.context.company.id
    else:
        return -1

@colander.deferred
def deferred_ccode_valid(node, kw):
    request = kw['request']
    company_id = get_company_id_from_request(request)
    client = get_client_from_request(request)

    def unique_ccode(node, value):
        """
            Test customer code unicity
        """
        if len(value) != 4:
            message = u"Le code client doit contenir 4 caractères."
            raise colander.Invalid(node, message)
        #Test unicity
        query = Client.query().filter(Client.company_id == company_id)\
                .filter(Client.code == value)
        if client:
            # In edit mode, it will always fail
            query = query.filter(Client.id != client.id)
        result = query.all()

        if len(result):
            message = u"Vous avez déjà utilisé ce code '{0}' pour un autre \
client".format(value)
            raise colander.Invalid(node, message)
    return unique_ccode


def remove_admin_fields(schema, kw):
    """
        Remove admin specific fields
    """
    if kw['request'].user.is_contractor():
        del schema['compte_cg']
        del schema['compte_tiers']


class ClientSchema(colander.MappingSchema):
    """
        Schema for customer insertion
    """
    name = colander.SchemaNode(colander.String(),
                            title=u"Nom de l'entreprise",
                            validator=colander.Length(max=255))
    code = colander.SchemaNode(colander.String(),
                             widget=widget.TextInputWidget(mask='****'),
                             title=u'Code',
                             validator=deferred_ccode_valid,
                             description=u"Ce code est unique")
    contactLastName = colander.SchemaNode(colander.String(),
                            title=u'Nom du contact principal',
                            validator=colander.Length(max=255))
    contactFirstName = colander.SchemaNode(colander.String(),
                        title=u"Prénom du contact principal",
                        missing=u"",
                        validator=colander.Length(max=255))
    function = colander.SchemaNode(colander.String(),
                        title=u"Fonction du contact principal",
                        missing=u"",
                        validator=colander.Length(max=255))
    email = get_mail_input(missing=u'')
    phone = colander.SchemaNode(colander.String(),
                                title=u'Téléphone',
                                missing=u'',
                                validator=colander.Length(max=50))
    fax = colander.SchemaNode(colander.String(),
                                title=u"Fax",
                                missing=u"",
                                validator=colander.Length(max=50))
    address = colander.SchemaNode(colander.String(),
                    title=u'Adresse',
                    missing=u'',
                    validator=colander.Length(max=255),
                    widget=widget.TextAreaWidget(cols=25, rows=1))
    zipCode = colander.SchemaNode(colander.String(),
                    title=u'Code postal',
                    missing=u'',
                    validator=colander.Length(max=20))
    city = colander.SchemaNode(colander.String(),
                    title=u'Ville',
                    missing=u'',
                    validator=colander.Length(max=255))
    country = colander.SchemaNode(colander.String(),
                title=u"Pays",
                missing=u'France',
                validator=colander.Length(max=255)
                )
    intraTVA = colander.SchemaNode(colander.String(),
                    title=u"TVA intracommunautaire",
                    validator=colander.Length(max=50),
                    missing=u'')
    # Fields specific to the treasury
    compte_cg = colander.SchemaNode(
            colander.String(),
            title=u"Compte CG",
            description=u"Compte CG utilisé pour ce client dans le logiciel \
de compta",
            missing="")
    compte_tiers = colander.SchemaNode(
            colander.String(),
            title=u"Compte Tiers du client",
            description=u"Compte Tiers utilisé pour ce client dans le logiciel \
de compta",
            missing="")
    comments = colander.SchemaNode(colander.String(),
            widget=widget.TextAreaWidget(cols=25, rows=2),
            title=u'Commentaires',
            missing=u'')


CLIENTSCHEMA = ClientSchema(after_bind=remove_admin_fields)


class ClientSearchSchema(BaseListsSchema):
    pass