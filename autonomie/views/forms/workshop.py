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
import colander
from deform import widget as deform_widget

from autonomie.models.workshop import STATUS
from autonomie.views.forms import (
    main,
    lists,
    activity,
    )


def get_info_field(title):
    """
    returns a simple node factorizing recurent datas
    """
    return colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=125),
        title=title,
        description=u"Utilisé dans la feuille d'émargement",
        missing="",
        )



class LeaderSequence(colander.SequenceSchema):
    name = colander.SchemaNode(
        colander.String(),
        title=u"Animateur/Animatrice",
        validator=colander.Length(max=100),
        )


def range_validator(form, values):
    """
    Ensure start_time is before end_time
    """
    if values['start_time'] >= values['end_time']:
        message = u"L'heure de début doit précéder celle de fin"
        exc = colander.Invalid(form, message)
        exc['start_time'] = u"Doit précéder la fin"
        raise exc


class TimeSlotSchema(colander.MappingSchema):
    id = main.id_node()
    name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=255),
        title=u"Intitulé",
        description=u"Intitulé utilisé dans la feuille d'émargement \
correspondante (ex: Matinée 1)",
    )
    start_time = main.now_node(title=u"Début de la tranche horaire")
    end_time = main.now_node(title=u"Fin de la tranche horaire")


class TimeSlotsSequence(colander.SequenceSchema):
    timeslot = TimeSlotSchema(
        title=u"Tranche horaire",
        validator=range_validator,
        )


class Workshop(colander.MappingSchema):
    """
    Schema for workshop creation/edition
    """
    come_from = main.come_from_node()
    name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=255),
        title=u"Titre de l'atelier",
        )
    leaders = LeaderSequence(
        title=u"Animateur(s)/Animatrice(s)",
        widget=deform_widget.SequenceWidget(min_len=1),
        )
    date = main.today_node(title=u"Date de l'atelier")
    info1 = get_info_field(u"Sous-titre 1 (facultatif)")
    info2 = get_info_field(u"Sous-titre 2 (facultatif)")
    info3 = get_info_field(u"Sous-titre 3 (facultatif)")
    participants = activity.ParticipantsSequence(
        title=u"Participants",
        widget=deform_widget.SequenceWidget(min_len=1),
        )
    timeslots = TimeSlotsSequence(
        title=u"Tranches horaires",
        description=u"Les différentes tranches horaires de l'atelier \
donnant lieu à un émargement",
        widget=deform_widget.SequenceWidget(min_len=1),
        )


def get_list_schema():
    """
    Return a schema for filtering workshop list
    """
    schema = lists.BaseListsSchema().clone()

    schema.insert(0,
        main.today_node(
            name='date',
            default=None,
            missing=None,
            description=u"Date de l'atelier",
            widget_options={'css_class': 'input-medium search-query'},
            ))

    schema.insert(0, main.user_node(
        missing=None,
        name='participant_id',
        widget_options={
            'placeholder': u"Sélectionner un participant",
            'default_option': (None, ''),
            }
        ))

    schema['search'].description = u"Intitulé de l'atelier"
    return schema


class AttendanceEntry(colander.MappingSchema):
    """
    Relationship edition
    Allows to edit the attendance status
    """
    account_id = main.id_node()
    timeslot_id = main.id_node()
    status = colander.SchemaNode(
        colander.String(),
        widget=deform_widget.SelectWidget(values=STATUS),
        validator=colander.OneOf(dict(STATUS).keys()),
        default='registered',
        missing='registered',
        )


class TimeSlotAttendanceEntries(colander.SequenceSchema):
    """
    """
    attendance = AttendanceEntry()


class Attendances(colander.MappingSchema):
    """
    Attendance registration schema
    """
    attendances = TimeSlotAttendanceEntries()
