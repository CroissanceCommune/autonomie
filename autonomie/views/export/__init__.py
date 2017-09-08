# -*-coding:utf-8-*-
# * Copyright (C) Coopérer pour entreprendre
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
import logging
from deform.exception import ValidationFailure

from autonomie.views import BaseView
from autonomie.compute.sage import MissingData

from autonomie.views.export.utils import HELPMSG_CONFIG


logger = logging.getLogger(__name__)


class BaseExportView(BaseView):
    """
    Base export view
    Provide skeleton for export view development

    - Return forms
    - Validate form datas
    - Check elements can be exported
    - Return error messages
    - Return the generated file
    """
    admin_route_name = "admin"

    def before(self):
        """
        Launched before anything is done
        """
        pass

    def get_forms(self):
        """
        :returns: the forms to be rendered in the form
            {formname: {'title': A title, 'form': 'The form object'}}
        :rtype: dict or OrderedDict
        """
        return {}

    def validate_form(self, forms):
        """
        Validate a submitted form if needed
        """
        form_name = appstruct = None
        if 'submit' in self.request.params:
            form_name = self.request.POST['__formid__']
            form = forms[form_name]['form']

            post_items = self.request.POST.items()

            logger.debug("Form %s was submitted", form_name)
            try:
                appstruct = form.validate(post_items)
            except ValidationFailure as validation_error:
                logger.exception(u"There was an error on form validation")
                logger.exception(post_items)
                # Replace the form, it now contains errors
                # - will be displayed again
                forms[form_name]['form'] = validation_error
        return form_name, appstruct

    def query(self, appstruct, form_name):
        """
        :param dict appstruct: The validated form datas
        :param str form_name: The name of the form that was submitted
        :returns: a Sqlalchemy query collecting items to be exported
        """
        raise NotImplemented()

    def check(self, items):
        """
        Check items are valid for export

        :param obj items: A Sqlalchemy query
        :returns: a 2-uple (valid, messages_dict) where messages_dict is in the
            form {'title': A message block title, "errors": [error messages]}
        """
        return True, {}

    def write_file(self, items):
        """
        Add a file to the request.response

        :param list items: the items to render
        :returns: A response object
        """
        raise NotImplemented()

    def record_exported(self, items, form_name, appstruct):
        """
        Record exported elements in the database

        :param list items: the items to render
        :param str form_name: The name of the form that was submitted
        :param dict appstruct: The validated datas
        """
        pass

    def __call__(self):
        """
        Main view entry

        1- Collect forms
        2- if submission :
            validate datas
            query
            check elements can be exported
            write the file
        3- return forms and messages
        """
        check_messages = None
        self.before()
        forms = self.get_forms()

        form_name, appstruct = self.validate_form(forms)

        if appstruct is not None:
            items = self.query(appstruct, form_name)
            is_ok, check_messages = self.check(items)

            if is_ok:
                try:
                    # Let's process and return successfully the csvfile
                    result = self.write_file(items, form_name, appstruct)
                    self.record_exported(items, form_name, appstruct)
                    return result
                except (MissingData, KeyError):
                    logger.exception("Exception occured while writing file")
                    config_help_msg = HELPMSG_CONFIG.format(
                        self.request.route_url(self.admin_route_name)
                    )
                    check_messages['errors'] = [config_help_msg]

        # We are either
        # * reporting an error
        # * or doing the initial display of forms.

        # rendered forms
        for key in forms:
            forms[key]['form'] = forms[key]['form'].render()

        return {
            'title': self.title,
            'check_messages': check_messages,
            'forms': forms,
        }
