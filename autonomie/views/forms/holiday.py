"""
    form schemas for holiday declaration
"""
import colander
import logging

from deform import widget
from autonomie.views.forms.widgets import deferred_autocomplete_widget
from autonomie.views.forms.widgets import get_date_input
from autonomie.models.user import User

log = logging.getLogger(__name__)


def date_validator(form, value):
    if value['start_date'] >= value['end_date']:
        exc = colander.Invalid(form,
                    u"La date de début doit précéder la date de fin")
        exc['start_date'] = u"Doit précéder la date de fin"
        raise exc


def get_user_choices():
    """
        Return the a list of values for the contractor autocomplete widget
    """
    choices = [(0, u'Tous les entrepreneurs')]
    choices.extend([(unicode(user.id),
                     u"{0} {1}".format(user.lastname, user.firstname),)
                        for user in User.query().all()])
    return choices

@colander.deferred
def deferred_contractor_list(node, kw):
    """
        Return the contractor list for selection in holiday search
        Needs to be deferred
    """
    choices = get_user_choices()
    return deferred_autocomplete_widget(node, {'choices':choices})


class HolidaySchema(colander.MappingSchema):
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début",
            widget=get_date_input())
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin",
            widget=get_date_input())


class HolidaysList(colander.SequenceSchema):
    holiday = HolidaySchema(title=u"Période", validator=date_validator)


class HolidaysSchema(colander.MappingSchema):
    holidays = HolidaysList(title=u"",
                widget=widget.SequenceWidget(min_len=1))


class SearchHolidaysSchema(colander.MappingSchema):
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début",
            widget=get_date_input())
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin",
            widget=get_date_input())
    user_id = colander.SchemaNode(colander.Integer(), title=u"Entrepreneur",
                       widget=deferred_contractor_list,
                       missing=None)


searchSchema = SearchHolidaysSchema(
                        title=u"Rechercher les congés des entrepreneurs",
                        validator=date_validator)