# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
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
from pyramid.httpexceptions import HTTPFound

from autonomie.forms.admin import (
    get_sequence_model_admin,
)
from autonomie.utils.ascii import (
    camel_case_to_name,
)
from autonomie.utils.widgets import ViewLink
from autonomie.views import (
    BaseFormView,
)


class AdminOption(BaseFormView):
    """
    Main view for option configuration
    It allows to configure a set of models

        factory

            The model we are manipulating.

        disable

            If the model has an "active" column, it can be used to
            enable/disable elements

        validation_msg

            The message shown to the end user on successfull validation

        redirect_path

            The route we're redirecting to after successfull validation
    """
    title = u""
    add_template_vars = ('message',)
    validation_msg = u""
    factory = None
    redirect_path = 'admin_index'
    disable = True
    _schema = None
    js_resources = []

    @property
    def schema(self):
        if self._schema is None:
            self._schema = get_sequence_model_admin(
                self.factory,
                self.title,
            )
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value

    @property
    def message(self):
        """
        Return an optionnal message to help to configure datas
        """
        calchemy_dict = getattr(self.factory, '__colanderalchemy_config__', {})
        return calchemy_dict.get('help_msg', '')

    def before(self, form):
        """
        Populate the form with existing elements
        """
        if not hasattr(self.js_resources, '__iter__'):
            self.js_resources = (self.js_resources,)

        for js_resource in self.js_resources:
            js_resource.need()

        appstruct = self.schema.dictify(self.factory.query().all())
        form.set_appstruct(appstruct)
        self.populate_actionmenu()

    def populate_actionmenu(self):
        self.request.actionmenu.add(
            ViewLink(u"Retour", path=self.redirect_path)
        )

    def _get_edited_elements(self, appstruct):
        """
        Return the elements that are edited (already have an id)
        """
        return dict(
            (data['id'], data)
            for data in appstruct.get('datas', {})
            if 'id' in data
        )

    def _disable_or_remove_elements(self, appstruct):
        """
        Disable existing elements that are no more in the results
        """
        edited = self._get_edited_elements(appstruct)

        for element in self.factory.query():
            if element.id not in edited.keys():
                if self.disable:
                    element.active = False
                    self.dbsession.merge(element)
                else:
                    self.dbsession.delete(element)

    def _add_or_edit(self, index, datas):
        """
        Add or edit an element of the given factory
        """
        node_schema = self.schema.children[0].children[0]
        element = node_schema.objectify(datas)
        element.order = index
        if element.id is not None:
            element = self.dbsession.merge(element)
        else:
            self.dbsession.add(element)
        return element

    def submit_success(self, appstruct):
        """
        Handle successfull submission
        """
        self._disable_or_remove_elements(appstruct)

        for index, datas in enumerate(appstruct.get('datas', [])):
            self._add_or_edit(index, datas)

        self.request.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path(self.redirect_path))


def get_model_admin_view(model, js_requirements=[], r_path="admin_userdatas"):
    """
    Return a view object and a route_name for administrating a sequence of
    models instances (like options)
    """
    infos = model.__colanderalchemy_config__
    view_title = infos.get('title', u'Titre inconnu')

    class MyView(AdminOption):
        title = view_title
        validation_msg = infos.get('validation_msg', u'')
        factory = model
        schema = get_sequence_model_admin(model, u"")
        redirect_path = r_path
        js_resources = js_requirements
    return (
        MyView,
        u"admin_%s" % camel_case_to_name(model.__name__),
        '/admin/main.mako',
    )


def add_link_to_menu(request, label, path, title):
    request.actionmenu.add(
        ViewLink(
            label,
            path=path,
            title=title,
        )
    )
