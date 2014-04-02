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
        )
from autonomie.views.forms import (
        main,
        lists,
        )


STATUS_OPTIONS = (
    (u"Tous les rendez-vous", "all"),
    (u"Planifiés", "planned"),
    (u"Participants absents", "absent"),
    (u"Participants excusés", "excused"),
    (u"Participants présents", "closed"),
    )

STATUSCHOICES = (
    ("closed", u"Participant(s) présents"),
    ("excused", u"Participant(s) excusés"),
    ("absent", u"Participant(s) absents"),
    )


def get_activity_types():
    return ActivityType.query().filter(ActivityType.active==True)


def get_activity_modes():
    return [mode.label for mode in ActivityMode.query()]


@colander.deferred
def deferred_select_type(node, kw):
    options = [(unicode(a.id), a.label) for a in get_activity_types()]
    return deform_widget.SelectWidget(values=options)


@colander.deferred
def deferred_select_mode(node, kw):
    modes = get_activity_modes()
    options = zip(modes, modes)
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
    participant_id = main.user_node(title=u"")


class CreateActivitySchema(colander.MappingSchema):
    """
        Activity creation schema
    """
    come_from = main.come_from_node()
    conseiller_id = main.user_node(
            title=u"Conseiller menant le rendez-vous",
            roles=['manager', 'admin'],
            )
    date = main.today_node(title=u"Date de rendez-vous")
    type_id = colander.SchemaNode(
            colander.Integer(),
            widget=deferred_select_type,
            title=u"Nature du rendez-vous",
            )
    action_label = colander.SchemaNode(
            colander.String(),
            title=u"Intitulé de l'action (financée)",
            validator=colander.Length(0, 125),
            )
    subaction_label = colander.SchemaNode(
            colander.String(),
            title=u"Intitulé sous-action",
            missing="",
            validator=colander.Length(0, 125),
            )
    mode = colander.SchemaNode(
            colander.String(),
            widget=deferred_select_mode,

            title=u"Mode d'entretien",
            )
    participants = ParticipantsSequence(
            title=u"Participants",
            widget=deform_widget.SequenceWidget(min_len=1))


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


class RecordActivitySchema(colander.Schema):
    """
    Schema for activity recording
    """
    status = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([x[0] for x in STATUSCHOICES]),
        widget=deform_widget.RadioChoiceWidget(values=STATUSCHOICES),
        title=u"Statut des participants",
        missing=u"closed")
    point = main.textarea_node(title=u"Point de suivi", missing='')
    objectifs = main.textarea_node(title=u"Définition des objectifs",
            missing='')
    action = main.textarea_node(title=u"Plan d'action et préconisations",
            missing='')
    documents = main.textarea_node(title=u"Documents produits", missing='')
    notes = main.textarea_node(title=u"Notes", missing="")


class ActivityListSchema(lists.BaseListsSchema):
    """
    Schema for activity listing
    """
    conseiller_id = main.user_node(
            roles=['manager', 'admin'],
            missing=-1,
            default=main.deferred_current_user_id,
            )
    participant_id = main.user_node(missing=-1)
    status = colander.SchemaNode(
            colander.String(),
            validator=colander.OneOf([s[1] for s in STATUS_OPTIONS]),
            default='all',
            missing='all')
    type_id = colander.SchemaNode(
            colander.Integer(),
            validator=deferred_type_validator,
            missing=-1)
