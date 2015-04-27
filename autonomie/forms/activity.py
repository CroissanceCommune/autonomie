# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
"""
    Activity related form schemas

    New activity creation
    Activity search schema
"""
import colander
import deform
import deform_extensions

from autonomie.models.activity import (
    ActivityType,
    ActivityMode,
    ActivityAction,
    STATUS_SEARCH,
    ATTENDANCE_STATUS,
    ATTENDANCE_STATUS_SEARCH,
)
from autonomie.models import user

from autonomie import forms
from autonomie.forms import lists


def get_activity_types():
    return ActivityType.query().filter(ActivityType.active==True)


def get_activity_modes():
    return [mode.label for mode in ActivityMode.query()]


def get_actions():
    query = ActivityAction.query()
    query = query.filter(ActivityAction.active==True)
    return query.filter(ActivityAction.parent_id==None)


def get_subaction_options():
    options = [("", "Sélectionner une sous-action"),]
    for action in get_actions():
        gr_options = [(unicode(a.id), a.label) for a in action.children]
        group = deform.widget.OptGroup(action.label, *gr_options)
        options.append(group)
    return options


def get_deferred_select_type(default=False):
    @colander.deferred
    def deferred_select_type(node, kw):
        values = [(unicode(a.id), a.label) for a in get_activity_types()]
        if default:
            values.insert(0, ("", 'Tous les rendez-vous'))
        return deform.widget.SelectWidget(values=values)
    return deferred_select_type


@colander.deferred
def deferred_select_mode(node, kw):
    modes = get_activity_modes()
    options = zip(modes, modes)
    return deform.widget.SelectWidget(values=options)


@colander.deferred
def deferred_select_action(node, kw):
    options = [("", u"Sélectionner une action"),]
    options.extend([(unicode(a.id), a.label) for a in get_actions()])
    return deform.widget.SelectWidget(values=options)


@colander.deferred
def deferred_select_subaction(node, kw):
    options = get_subaction_options()
    return deform.widget.SelectWidget(values=options)


@colander.deferred
def deferred_type_validator(node, kw):
    values = [a.id for a in get_activity_types()]
    values.append(-1)
    return colander.OneOf(values)


@colander.deferred
def deferred_mode_validator(node, kw):
    values = [a.label for a in get_activity_modes()]
    values.append(-1)
    return colander.OneOf(values)


class ParticipantsSequence(colander.SequenceSchema):
    """
    Schema for the list of participants
    """
    participant_id = user.user_node(title=u"", )


class ConseillerSequence(colander.SequenceSchema):
    """
    Schema for the list of conseiller
    """
    conseiller_id = user.user_node(
        title=u"Conseillers menant le rendez-vous",
        roles=['manager', 'admin'],
    )


class CreateActivitySchema(colander.MappingSchema):
    """
        Activity creation schema
    """
    come_from = forms.come_from_node()

    conseillers = ConseillerSequence(
        title=u"Conseillers",
        widget=deform.widget.SequenceWidget(min_len=1)
    )
    datetime = forms.now_node(title=u"Date de rendez-vous")
    type_id = colander.SchemaNode(
        colander.Integer(),
        widget=get_deferred_select_type(),
        title=u"Nature du rendez-vous",
    )
    action_id = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_select_action,
        title=u"Intitulé de l'action (financée)",
    )
    subaction_id = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_select_subaction,
        title=u"Intitulé sous-action",
        missing=None,
    )
    mode = colander.SchemaNode(
        colander.String(),
        widget=deferred_select_mode,
        title=u"Mode d'entretien",
    )
    participants = ParticipantsSequence(
        title=u"Participants",
        widget=deform.widget.SequenceWidget(min_len=1)
    )


class NewActivitySchema(CreateActivitySchema):
    """
        New activity Schema, used to initialize an activity, provides an option
        to start it directly
    """
    now = colander.SchemaNode(
            colander.Boolean(),
            title=u"Démarrer le rendez-vous immédiatement",
            default=False,
            )


class Attendance(colander.MappingSchema):
    account_id = forms.id_node()
    event_id = forms.id_node()

    username = colander.SchemaNode(
        colander.String(),
        title=u'',
        widget=deform_extensions.DisabledInput(),
        missing='',
        )

    status = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RadioChoiceWidget(values=ATTENDANCE_STATUS),
        validator=colander.OneOf([x[0] for x in ATTENDANCE_STATUS]),
        title=u'',
        missing=u'excused',
        )


class Attendances(colander.SequenceSchema):
    attendance = Attendance(
        title=u'',
        widget=deform_extensions.InlineMappingWidget()
        )


class RecordActivitySchema(colander.Schema):
    """
    Schema for activity recording
    """
    attendances = Attendances(
        title=u'Présence',
        widget=deform.widget.SequenceWidget(
            template='autonomie:deform_templates/fixed_len_sequence.pt',
            item_template='autonomie:deform_templates/fixed_len_sequence_item.pt')
    )

    objectifs = forms.textarea_node(
        title=u"Objectifs du rendez-vous",
        richwidget=True,
        missing='',
        )

    point = forms.textarea_node(
        title=u"Points abordés",
        richwidget=True,
        missing='',
        )

    action = forms.textarea_node(
        title=u"Plan d'action et préconisations",
        richwidget=True,
        missing='',
        )

    documents = forms.textarea_node(
        title=u"Documents produits",
        richwidget=True,
        missing='',
        )

    notes = forms.textarea_node(
        title=u"Notes",
        richwidget=True,
        missing="",
        )

    duration = colander.SchemaNode(
        colander.Integer(),
        title=u'Durée',
        description=u"La durée du rendez-vous, en minute (ex : 90)",
        widget=deform.widget.TextInputWidget(
            input_append='minutes',
        ),
    )


def get_list_schema(is_admin=False):
    schema = lists.BaseListsSchema().clone()

    schema.insert(0, colander.SchemaNode(
        colander.Integer(),
        name='type_id',
        widget=get_deferred_select_type(True),
        validator=deferred_type_validator,
        missing=colander.drop))

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name='status',
        widget=deform.widget.SelectWidget(values=STATUS_SEARCH),
        validator=colander.OneOf([s[0] for s in STATUS_SEARCH]),
        missing=colander.drop))

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name='user_status',
        widget=deform.widget.SelectWidget(values=ATTENDANCE_STATUS_SEARCH),
        validator=colander.OneOf([s[0] for s in ATTENDANCE_STATUS_SEARCH]),
        missing=colander.drop))


    if is_admin:
        schema.insert(0, user.user_node(
            missing=colander.drop,
            name='participant_id',
            widget_options={
                'default_option': ("", u"- Sélectionner un participant -"),
            }
            )
        )

        schema.insert(0, user.user_node(
            roles=['manager', 'admin'],
            missing=colander.drop,
            name='conseiller_id',
            widget_options={
                'default_option': ("", u"- Sélectionner un conseiller -"),
            }
            )
        )

    del schema['search']
    return schema
