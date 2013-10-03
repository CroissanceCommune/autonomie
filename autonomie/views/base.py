# -*- coding: utf-8 -*-
# * File Name : base.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 24-04-2012
# * Last Modified :
#
# * Project :
#
"""
    Base views with commonly used utilities
"""
import inspect
import logging
import colander

from functools import partial

from sqlalchemy import desc, asc

from webhelpers import paginate

from autonomie.utils.views import get_page_url
from autonomie.views.forms.lists import ITEMS_PER_PAGE_OPTIONS
from autonomie.export.csvtools import SqlaToCsvWriter
from autonomie.export.utils import write_file_to_request


log = logging.getLogger(__name__)


class BaseView(object):
    def __init__(self, request):
        self.request = request
        self.session = self.request.session

class BaseListView(BaseView):
    """
        A base list view used to provide an easy way to list elements

        * It launches a query to retrieve records
        * Validates GET params regarding the given schema
        * filter the query with the provided filter_* methods
        * Launches complementary methods to populate request vars like popup
          or actionmenu

        @param add_template_vars: list of attributes (or properties)
                                  that will be automatically added
                                  to the response dict

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
    add_template_vars = ('title',)
    schema = None
    default_sort = 'name'
    sort_columns = {'name':'name'}
    default_direction = 'asc'

    def query(self):
        """
            The main query, should be overrided by a subclass
        """
        pass

    def _get_filters(self):
        """
            Return the list of the filter_... methods attached to the current
            object
        """
        for method_name, method in inspect.getmembers(self, inspect.ismethod):
            if method_name.startswith('filter_'):
                yield method

    def _filter(self, query, appstruct):
        """
            filter the query with the configured filters
        """
        for method in self._get_filters():
            print method
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

    def __call__(self):
        """
            This method is a used in pyramid to make a class a view
        """
        query = self.query()
        schema = self.schema.bind(**self._get_bind_params())
        try:
            appstruct = schema.deserialize(self.request.GET)
        except colander.Invalid:
            # If values are not valid, we want the default ones to be provided
            # see the schema definition
            appstruct = schema.deserialize({})

        query = self._filter(query, appstruct)
        query = self._sort(query, appstruct)
        records = self._paginate(query, appstruct)
        result = dict(records=records)
        result.update(self.default_form_values(appstruct))
        result.update(self.more_template_vars())
        self.populate_actionmenu(appstruct)
        return result

    def default_form_values(self, appstruct):
        """
            Return the default value to pass to the forms
            Here we return the items_per_page_options and the appstruct
        """
        appstruct['items_per_page_options'] = ITEMS_PER_PAGE_OPTIONS
        return appstruct

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


class BaseCsvView(BaseView):
    """
        Base Csv view

        Launches the appropriate query and store the whole stuff in a csv file
    """
    model = None
    csvwriter = SqlaToCsvWriter

    @property
    def filename(self):
        """
            To be implemented by the subclasse
        """
        pass

    def query(self):
        """
            To be implemented by the subclasse
        """
        pass

    def __call__(self):
        writer = self.csvwriter(self.model)
        for item in self.query():
            writer.add_row(item.appstruct())
        write_file_to_request(self.request, self.filename, writer.render())
        return self.request.response

