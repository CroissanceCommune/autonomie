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
    Base views with commonly used utilities
"""
import inspect
import logging
import colander
import itertools

from deform import Form
from deform import Button
from pyramid_deform import FormView
from pyramid.security import has_permission
from js.tinymce import tinymce

from functools import partial
from sqlalchemy import desc, asc
from webhelpers import paginate
from pyramid.url import current_route_url

from autonomie.forms import merge_session_with_post, flatten_appstruct
from autonomie.forms.lists import ITEMS_PER_PAGE_OPTIONS
from autonomie.export.csvtools import SqlaCsvExporter
from autonomie.export.excel import SqlaXlsExporter
from autonomie.export.utils import write_file_to_request


submit_btn = Button(name="submit", type="submit", title=u"Valider")
cancel_btn = Button(name="cancel", type="submit", title=u"Annuler")


log = logging.getLogger(__name__)


def get_page_url(request, page):
    """
        Return a url generator for pagination
    """
    args = request.GET
    args['page'] = str(page)
    return current_route_url(request, page=page, _query=args)


class BaseView(object):
    def __init__(self, context, request=None):
        if request is None:
            # Needed for manually called views
            self.request = context
            self.context = self.request.context
        else:
            self.request = request
            self.context = context
        self.session = self.request.session


class BaseListClass(BaseView):
    """
    Base class for list related views (list view and exports)

        * It launches a query to retrieve records
        * Validates GET params regarding the given schema
        * filter the query with the provided filter_* methods

    @param schema: Schema used to validate the GET params provided in the
                    url, the schema should inherit from
                    autonomie.views.forms.lists.BaseListsSchema to preserve
                    most of the processed automation
    @param sort_columns: dict of {'sort_column_key':'sort_column'...}.
        Allows to generate the validator for the sort availabilities and
        to automatically add a order_by clause to the query. sort_column
        may be equal to Table.attribute if join clauses are present in the
        main query.
    @default_sort: the default sort_column_key to be used
    @default_direction: the default sort direction (one of ['asc', 'desc'])

    A subclass shoud provide at least a schema and a query method
    """
    schema = None
    default_sort = 'name'
    sort_columns = {'name':'name'}
    default_direction = 'asc'

    def _get_bind_params(self):
        """
        return the params passed to the form schema's bind method
        if subclass override this method, it should call the super
        one's too
        """
        return dict(request=self.request,
                    default_sort=self.default_sort,
                    default_direction=self.default_direction,
                    sort_columns=self.sort_columns)

    def query(self):
        """
        The main query, should be overrided by a subclass
        """
        pass

    def _get_filters(self):
        """
        collect the filter_... methods attached to the current object
        """
        for method_name, method in inspect.getmembers(self, inspect.ismethod):
            if method_name.startswith('filter_'):
                yield method

    def _filter(self, query, appstruct):
        """
        filter the query with the configured filters
        """
        for method in self._get_filters():
            query = method(query, appstruct)
        return query

    def _sort(self, query, appstruct):
        """
        Sort the results regarding the default values and
        the sort_columns dict, maybe overriden to provide a custom sort
        method
        """
        sort_column_key = appstruct['sort']
        sort_column = self.sort_columns[sort_column_key]

        sort_direction = appstruct['direction']
        if sort_direction == 'asc':
            func = asc
        else:
            func = desc
        return query.order_by(func(sort_column))

    def _collect_appstruct(self):
        """
        collect the filter options from the current url

        Use the schema to validate the GET params of the current url and returns
        the formated datas
        """
        schema = None
        appstruct = {}
        if self.schema is not None:
            schema = self.schema.bind(**self._get_bind_params())
            try:
                appstruct = schema.deserialize(self.request.GET)
            except colander.Invalid as e:
                # If values are not valid, we want the default ones to be provided
                # see the schema definition
                log.error("CURRENT SEARCH VALUES ARE NOT VALID")
                log.error(e)
                appstruct = schema.deserialize({})
        return schema, appstruct

    def __call__(self):
        schema, appstruct = self._collect_appstruct()

        query = self.query()
        query = self._filter(query, appstruct)
        query = self._sort(query, appstruct)

        return self._build_return_value(schema, appstruct, query)

    def _build_return_value(self, schema, appstruct, query):
        """
        To be implemented : datas returned by the view
        """
        return {}


class BaseListView(BaseListClass):
    """
    A base list view used to provide an easy way to build list views
    Uses the BaseListClass and add the templating datas :

        * Provide a pagination object
        * Provide a search form based on the given schema
        * Launches complementary methods to populate request vars like popup
        or actionmenu

    @param add_template_vars: list of attributes (or properties)
                                that will be automatically added
    """
    add_template_vars = ('title',)

    def _paginate(self, query, appstruct):
        """
            wraps the current SQLA query with pagination
        """
        # Url builder for page links
        page_url = partial(get_page_url, request=self.request)
        current_page = appstruct['page']
        items_per_page = appstruct['items_per_page']
        return paginate.Page(query,
                             current_page,
                             url=page_url,
                             items_per_page=items_per_page)

    def get_form(self, schema, appstruct):
        # counter is used to avoid field name conflicts
        form = Form(schema, counter=itertools.count(15000))
        form.widget.template = "autonomie:deform_templates/searchform.pt"
        return form.render(appstruct)

    def more_template_vars(self):
        """
            Add template vars to the response dict
            List the attributes configured in the add_template_vars attribute
            and add them
        """
        result = {}
        for name in self.add_template_vars:
            result[name] = getattr(self, name)
        return result

    def populate_actionmenu(self, appstruct):
        """
            Used to populate an actionmenu (if there's one in the page)
            actionmenu is a request attribute used to automate the integration
            of actionmenus in pages
        """
        pass

    def _build_return_value(self, schema, appstruct, query):
        """
        Return the datas expected by the template
        """
        records = self._paginate(query, appstruct)
        result = dict(records=records)
        result['form'] = self.get_form(schema, appstruct)
        result.update(self.more_template_vars())
        self.populate_actionmenu(appstruct)
        return result


class BaseCsvView(BaseListClass):
    """
        Base Csv view

        A list view that returns a streamed file

        A subclass should implement :

            * a query method
            * filename property

        To be able to handle the rows that are streamed:

            * a _stream_rows method

        If this view should support the GET params filtering method (export
        associated to a list view), a subclass should provide:

            * a schema attr
            * filter_ methods
    """
    model = None
    writer = SqlaCsvExporter

    @property
    def filename(self):
        """
        To be implemented by the subclass
        """
        pass

    def _stream_rows(self, query):
        """
        Return a generator with the rows we expect in our output,
        default is to return the sql ones
        """
        for item in query.all():
            yield item


    def _init_writer(self):
        return self.writer(self.model)

    def _build_return_value(self, schema, appstruct, query):
        """
        Return the streamed file object
        """
        writer = self._init_writer()
        for item in self._stream_rows(query):
            writer.add_row(item)

        write_file_to_request(self.request, self.filename, writer.render())
        return self.request.response


class BaseXlsView(BaseCsvView):
    writer = SqlaXlsExporter


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
    title = None
    add_template_vars = ()
    buttons = (submit_btn,)

    def __init__(self, request):
        super(BaseFormView, self).__init__(request)
        self.context = request.context
        self.dbsession = self.request.dbsession
        self.session = self.request.session
        self.logger = logging.getLogger("form_admin")
        if has_permission('manage', request.context, request):
            tinymce.need()

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
        # Force title in template vars
        result['title'] = self.title

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
        return form

    def submit_failure(self, e):
        """
        Called by default when we failed to submit the values
        We add a token here for forms that are collapsed by default to keep them
        open if there is an error
        """
        # On loggue l'erreur colander d'origine
        log.exception(e.error)
        return dict(form=e.render(), formerror=True)
