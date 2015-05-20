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
import deform
from deform import widget as deform_widget

from autonomie.models.activity import ATTENDANCE_STATUS
from autonomie.models.workshop import WorkshopAction
from autonomie.models import user
from autonomie import forms
from autonomie.forms import lists, activity


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


def get_info1():
    query = WorkshopAction.query()
    query = query.filter(WorkshopAction.active==True)
    return query.filter(WorkshopAction.parent_id==None)


@colander.deferred
def deferred_info1(node, kw):
    options = [(unicode(a.id), a.label) for a in get_info1()]
    return deform.widget.SelectWidget(values=options)


@colander.deferred
def deferred_info2(node, kw):
    options = [("", u"- Sélectionner un sous-titre -")]
    for info1 in get_info1():
        if info1.children:
            group_options = [(unicode(a.id), a.label) for a in info1.children]
            group = deform.widget.OptGroup(info1.label, *group_options)
            options.append(group)
    return deform.widget.SelectWidget(values=options)


@colander.deferred
def deferred_info3(node, kw):
    options = [("", u"- Sélectionner un sous-titre -")]
    for info1 in get_info1():
        for info2 in info1.children:
            group_label = u"{1}".format(info1.label, info2.label)
            group_options = [(unicode(a.id), a.label) for a in info2.children]
            group = deform.widget.OptGroup(group_label, *group_options)
            options.append(group)
    return deform.widget.SelectWidget(values=options)


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


class TimeslotSchema(colander.MappingSchema):
    id = forms.id_node()
    name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=255),
        title=u"Intitulé",
        description=u"Intitulé utilisé dans la feuille d'émargement \
correspondante (ex: Matinée 1)",
    )
    start_time = forms.now_node(title=u"Début de la tranche horaire")
    end_time = forms.now_node(title=u"Fin de la tranche horaire")


class TimeslotsSequence(colander.SequenceSchema):
    timeslot = TimeslotSchema(
        title=u"Tranche horaire",
        validator=range_validator,
        )


class Workshop(colander.MappingSchema):
    """
    Schema for workshop creation/edition
    """
    come_from = forms.come_from_node()
    name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=255),
        title=u"Titre de l'atelier",
        )
    leaders = LeaderSequence(
        title=u"Animateur(s)/Animatrice(s)",
        widget=deform_widget.SequenceWidget(min_len=1),
        )
    info1_id = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_info1,
        title=u"Intitulé de l'action financée 1",
        description=u"Utilisée comme titre dans la sortie PDF",
    )
    info2_id = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_info2,
        title=u"Intitulé de l'action financée 2",
        description=u"Utilisée comme sous-titre dans la sortie PDF",
        missing=colander.drop,
    )
    info3_id = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_info3,
        title=u"Intitulé de l'action financée 3",
        description=u"Utilisée comme second sous-titre dans la sortie PDF",
        missing=colander.drop,
    )
    participants = activity.ParticipantsSequence(
        title=u"Participants",
        widget=deform_widget.SequenceWidget(min_len=1),
        )
    timeslots = TimeslotsSequence(
        title=u"Tranches horaires",
        description=u"Les différentes tranches horaires de l'atelier \
donnant lieu à un émargement",
        widget=deform_widget.SequenceWidget(min_len=1),
        )


def get_list_schema(company=False):
    """
    Return a schema for filtering workshop list
    """
    schema = lists.BaseListsSchema().clone()

    schema.insert(0,
        forms.today_node(
            name='date',
            default=colander.null,
            missing=colander.drop,
            description=u"Date de l'atelier",
            widget_options={'css_class': 'input-medium search-query'},
            ))

    if not company:
        schema.insert(0, user.user_node(
            missing=colander.drop,
            name='participant_id',
            widget_options={
                'default_option': ('', u"- Sélectionner un participant -"),
                }
        ))

    schema['search'].description = u"Intitulé de l'atelier"
    return schema


class AttendanceEntry(colander.MappingSchema):
    """
    Relationship edition
    Allows to edit the attendance status
    """
    account_id = forms.id_node()
    timeslot_id = forms.id_node()
    status = colander.SchemaNode(
        colander.String(),
        widget=deform_widget.SelectWidget(values=ATTENDANCE_STATUS),
        validator=colander.OneOf(dict(ATTENDANCE_STATUS).keys()),
        default='registered',
        missing='registered',
        )


class TimeslotAttendanceEntries(colander.SequenceSchema):
    """
    """
    attendance = AttendanceEntry()


class Attendances(colander.MappingSchema):
    """
    Attendance registration schema
    """
    attendances = TimeslotAttendanceEntries()
