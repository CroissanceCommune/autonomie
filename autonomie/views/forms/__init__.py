# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
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
#

"""
    Form view tool to easily build form views
"""


import colander
import logging

from pyramid_deform import FormView
from autonomie.utils.views import submit_btn

class BaseFormView(FormView):
    """
        Allows to easily build form views

        **Attributes that you may override**

        .. attribute:: add_template_vars

            List of attribute names (or properties) that will be added to the
            result dict object and that you will be able to use in your
            templates (('title',) by default)

        .. attribute:: buttons

            list or tupple of deform.Button objects (or strings), only a submit
            button is added by default

        .. attribute:: schema

            colander form schema to be used to render our form

        .. attribute:: form_class

            form class to use (deform.Form by default)

        **Methods that your should implement**

        .. method:: <button_name>_success(appstruct)

            Is called when the form has been submitted and validated with
            the button called button_name.

            *appstruct* : the colander validated datas (a dict)

        **Methods that you may implement**

        .. method:: before(form)

            Allows to execute some code before the validation process
            e.g: add datas to the form that will be rendered
            Will typically be overrided in an edit form.

            *form* : the form object that's used in our view

        .. method:: <button_name>_failure(e)

            Is called when the form has been submitted the button called
            button_name and the datas have not been validated.

            *e* : deform.exception.ValidationFailure that has
                been raised by colander

        .. code-block:: python

            class MyFormView(BaseFormView):
                title = u"My form view"
                schema = MyColanderSchema

                def before(self, form):
                    form.set_appstruct(self.request.context.appstruct())

                def submit_success(self, appstruct):
                    # Handle the filtered appstruct
    """
    add_template_vars = ('title',)
    buttons = (submit_btn,)

    def __init__(self, request):
        super(BaseFormView, self).__init__(request)
        self.dbsession = self.request.dbsession
        self.session = self.request.session
        self.logger = logging.getLogger("form_admin")

    def __call__(self):
        try:
            result = super(BaseFormView, self).__call__()
        except colander.Invalid, exc:
            self.logger.exception(
                "Exception while rendering form "
                "'%s': %s - struct received: %s",
                self.title, exc, self.appstruct())
            raise
        if isinstance(result, dict):
            result.update(self._more_template_vars())
        return result

    def _more_template_vars(self):
        """
            Add template vars to the response dict
        """
        result = {}
        for name in self.add_template_vars:
            result[name] = getattr(self, name)
        return result

    def _get_form(self):
        """
            A simple hack to be able to retrieve the form once again
        """
        use_ajax = getattr(self, 'use_ajax', False)
        ajax_options = getattr(self, 'ajax_options', '{}')
        self.schema = self.schema.bind(**self.get_bind_data())
        form = self.form_class(self.schema, buttons=self.buttons,
                        use_ajax=use_ajax, ajax_options=ajax_options,
                        **dict(self.form_options))
        self.before(form)



def merge_session_with_post(session, app_struct):
    """
        Merge Deform validated datas with SQLAlchemy's objects
        Allow to spare some lines of assigning datas to the object
        before writing to database
    """
    for key, value in app_struct.items():
        setattr(session, key, value)
    return session


def flatten_appstruct(appstruct):
    """
        return a flattened appstruct, suppose all keys in the dict and subdict
        are unique
    """
    res = {}
    for key, value in appstruct.items():
        if not isinstance(value, dict):
            res[key] = value
        else:
            res.update(value)
    return res
