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
from deform import widget

from autonomie.models.activity import (
        ActivityType,
        ACTIVITY_MODES,
        )
from autonomie.views.forms import (
        main,
        lists,
        )


STATUS_OPTIONS = (
    (u"Toutes les activités", "all"),
    (u"Les activités planifiées", "planned"),
    (u"Les activités terminées", "closed"),
    )



def get_activity_types():
    return ActivityType.query().filter(ActivityType.active==True)


@colander.deferred
def deferred_select_type(node, kw):
    options = [(unicode(a.id), a.label) for a in get_activity_types()]
    return widget.SelectWidget(values=options)


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
            title=u"Conseiller menant l'activité",
            roles=['manager', 'admin'],
            )
    date = main.today_node(title=u"Date de l'activité")
    type_id = colander.SchemaNode(
            colander.Integer(),
            widget=deferred_select_type,
            title=u"Type d'activité",
            )
    mode = colander.SchemaNode(
            colander.String(),
            widget=widget.SelectWidget(values=zip(ACTIVITY_MODES, ACTIVITY_MODES)),
            title=u"Mode d'entretien",
            )
    participants = ParticipantsSequence(title=u"Participants",
            widget=widget.SequenceWidget(min_len=1))


class NewActivitySchema(CreateActivitySchema):
    """
        New activity Schema, used to initialize an activity, provides an option
        to start it directly
    """
    now = colander.SchemaNode(
            colander.Boolean(),
            title=u"Démarrer l'activité immédiatement",
            default=False,
            )


class RecordActivitySchema(colander.Schema):
    """
    Schema for activity recording
    """
    point = main.textarea_node(title=u"Point de suivi")
    objectifs = main.textarea_node(title=u"Définition des objectifs")
    action = main.textarea_node(title=u"Plan d'action et préconisations")
    documents = main.textarea_node(title=u"Documents produits")


class ActivityListSchema(lists.BaseListsSchema):
    """
    Schema for activity listing
    """
    status = colander.SchemaNode(
            colander.String(),
            validator=colander.OneOf([s[1] for s in STATUS_OPTIONS]),
            default='all',
            missing='all')
    conseiller_id = main.user_node(
            roles=['manager', 'admin'],
            missing=-1,
            default=main.deferred_current_user_id,
            )
    participant_id = main.user_node(missing=-1)
