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
    Activity search schema (#TODO)
"""
import colander
from deform import widget as deform_widget

from autonomie.models.activity import (
        ActivityType,
        ActivityMode,
        ActivityAction,
        STATUS_SEARCH,
        ATTENDANCE_STATUS,
        ATTENDANCE_STATUS_SEARCH,
        )

from autonomie.views.forms import (
        main,
        lists,
        widgets as custom_widget,
        )


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
        group = deform_widget.OptGroup(action.label, *gr_options)
        options.append(group)
    return options


def get_deferred_select_type(default=False):
    @colander.deferred
    def deferred_select_type(node, kw):
        values = [(unicode(a.id), a.label) for a in get_activity_types()]
        if default:
            values.insert(0, (-1, 'Tous'))
        return deform_widget.SelectWidget(values=values)
    return deferred_select_type


@colander.deferred
def deferred_select_mode(node, kw):
    modes = get_activity_modes()
    options = zip(modes, modes)
    return deform_widget.SelectWidget(values=options)


@colander.deferred
def deferred_select_action(node, kw):
    options = [("", u"Sélectionner une action"),]
    options.extend([(unicode(a.id), a.label) for a in get_actions()])
    return deform_widget.SelectWidget(values=options)


@colander.deferred
def deferred_select_subaction(node, kw):
    options = get_subaction_options()
    return deform_widget.SelectWidget(values=options)


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
    participant_id = main.user_node(title=u"", )


class ConseillerSequence(colander.SequenceSchema):
    """
    Schema for the list of conseiller
    """
    conseiller_id = main.user_node(
        title=u"Conseillers menant le rendez-vous",
        roles=['manager', 'admin'],
    )


class CreateActivitySchema(colander.MappingSchema):
    """
        Activity creation schema
    """
    come_from = main.come_from_node()

    conseillers = ConseillerSequence(
        title=u"Conseillers",
        widget=deform_widget.SequenceWidget(min_len=1)
    )
    datetime = main.now_node(title=u"Date de rendez-vous")
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
        widget=deform_widget.SequenceWidget(min_len=1)
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
    account_id = main.id_node()
    event_id = main.id_node()

    username = colander.SchemaNode(
        colander.String(),
        title=u'',
        widget=custom_widget.DisabledInput(),
        missing='',
        )

    status = colander.SchemaNode(
        colander.String(),
        widget=deform_widget.RadioChoiceWidget(values=ATTENDANCE_STATUS),
        validator=colander.OneOf([x[0] for x in ATTENDANCE_STATUS]),
        title=u'',
        missing=u'excused',
        )


class Attendances(colander.SequenceSchema):
    attendance = Attendance(
        title=u'',
        widget=custom_widget.InlineMappingWidget()
        )


class RecordActivitySchema(colander.Schema):
    """
    Schema for activity recording
    """
    attendances = Attendances(
        title=u'Présence',
        widget=deform_widget.SequenceWidget(
            template='autonomie:deform_templates/fixed_len_sequence.pt',
            item_template='autonomie:deform_templates/fixed_len_sequence_item.pt')
    )
    point = main.textarea_node(
        title=u"Point de suivi",
        richwidget=True,
        missing='',
        )

    objectifs = main.textarea_node(
        title=u"Définition des objectifs",
        richwidget=True,
        missing='',
        )

    action = main.textarea_node(
        title=u"Plan d'action et préconisations",
        richwidget=True,
        missing='',
        )

    documents = main.textarea_node(
        title=u"Documents produits",
        richwidget=True,
        missing='',
        )

    notes = main.textarea_node(
        title=u"Notes",
        richwidget=True,
        missing="",
        )

    duration = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=6),
        title=u'Durée',
        description=u"La durée du rendez-vous (ex : 1h30)")


def get_list_schema():
    schema = lists.BaseListsSchema().clone()

    schema.insert(0, colander.SchemaNode(
        colander.Integer(),
        name='type_id',
        widget=get_deferred_select_type(True),
        validator=deferred_type_validator,
        missing=-1))

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name='status',
        widget=deform_widget.SelectWidget(values=STATUS_SEARCH),
        validator=colander.OneOf([s[0] for s in STATUS_SEARCH]),
        default='all',
        missing='all'))

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name='user_status',
        widget=deform_widget.SelectWidget(values=ATTENDANCE_STATUS_SEARCH),
        validator=colander.OneOf([s[0] for s in ATTENDANCE_STATUS_SEARCH]),
        default='all',
        missing='all'))


    schema.insert(0, main.user_node(
        missing=-1,
        name='participant_id',
        widget_options={
            'default_option': (-1, ''),
            'placeholder': u"Sélectionner un participant"},
        )
    )

    schema.insert(0, main.user_node(
        roles=['manager', 'admin'],
        missing=-1,
        default=main.deferred_current_user_id,
        name='conseiller_id',
        widget_options={
            'default_option': (-1, ''),
            'placeholder': u"Sélectionner un conseiller"},
        )
    )

    del schema['search']
    return schema
