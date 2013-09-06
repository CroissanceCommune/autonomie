# -*- coding: utf-8 -*-
# * File Name : __init__.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-04-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Form view tool to easily build form views
"""
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

    def __call__(self):
        result = super(BaseFormView, self).__call__()
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


def merge_session_with_post(session, app_struct):
    """
        Merge Deform validated datas with SQLAlchemy's objects
        Allow to spare some lines of assigning datas to the object
        before writing to database
    """
    for key, value in app_struct.items():
        setattr(session, key, value)
    return session

