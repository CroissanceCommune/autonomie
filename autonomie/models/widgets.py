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
Widget and usefull declaration to be used with colanderalchemy schemas
declaration

colanderalchemy allows to provide colander schema declaration directly in the
models, here we provide some usefull declarations
"""
import colander
from deform import widget as deform_widget
from autonomie.utils import form_widget as custom_widget


EXCLUDED = {'exclude': True}


MAIL_ERROR_MESSAGE = u"Veuillez entrer une adresse e-mail valide"


def get_hidden_field_conf():
    """
    Return the model's info conf to get a colanderalchemy hidden widget
    """
    return {
            'widget': deform_widget.HiddenWidget(),
            'missing': None
    }


def get_deferred_select_validator(model):
    """
    Return a deferred validator based on the given model

        model

            Option model having at least two attributes id and label
    """
    @colander.deferred
    def deferred_validator(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        return colander.OneOf([m.id for m in model.query()])
    return deferred_validator


def get_deferred_select(model, multi=False):
    """
    Return a deferred select widget based on the given model

        model

            Option model having at least two attributes id and label
    """
    @colander.deferred
    def deferred_widget(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        values = [(m.id, m.label) for m in model.query()]
        return deform_widget.SelectWidget(values=values, multi=multi)
    return deferred_widget


def get_select(options, multi=False):
    """
    Return a select widget with the provided options

        options

            options as expected by the deform select widget (a sequence of
            2-uples: (id, label))
    """
    return deform_widget.SelectWidget(values=options, multi=False)


def get_select_validator(options):
    """
    return a validator for the given options

        options

            options as expected by the deform select widget (a sequence of
            2-uples : (id, label))

    """
    return colander.OneOf([o[0] for o in options])


def get_date():
    """
    Return a date selection widget
    """
    return custom_widget.CustomDateInputWidget(css_class='span2')


def mail_validator():
    """
    Return an email entry validator with a custom error message
    """
    return colander.Email(MAIL_ERROR_MESSAGE)
