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
import deform
import deform_extensions
import itertools

from deform import Form
from deform import Button
from deform_extensions import GridFormWidget
from pyramid_deform import (
    FormView,
    CSRFSchema,
)
from pyramid.httpexceptions import HTTPFound
from js.tinymce import tinymce

from sqlalchemy import desc, asc
from webhelpers import paginate

from sqla_inspect.csv import SqlaCsvExporter
from sqla_inspect.excel import SqlaXlsExporter
from sqla_inspect.ods import SqlaOdsExporter
from autonomie.utils.renderer import set_close_popup_response
from autonomie.compute.math_utils import convert_to_int
from autonomie.export.utils import write_file_to_request
from autonomie.utils import rest
from autonomie.utils.widgets import Link


logger = logging.getLogger(__name__)


submit_btn = Button(
    name="submit",
    type="submit",
    title=u"Valider",
    css_class='btn btn-success primary-action'
)
cancel_btn = Button(
    name="cancel",
    type="submit",
    title=u"Annuler",
    css_class='btn btn-default'
)


class BaseView(object):
    def __init__(self, context, request=None):
        self.logger = logging.getLogger("autonomie.views.__init__")

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
    sort_columns = {'name': 'name'}
    default_direction = 'asc'
    grid = None
    filter_button_label = u"Filtrer"

    def __init__(self, *args, **kwargs):
        BaseView.__init__(self, *args, **kwargs)
        self.error = None

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
        for key in dir(self):
            if key.startswith('filter_'):
                func = getattr(self, key)
                if inspect.ismethod(func):
                    yield func

    def _filter(self, query, appstruct):
        """
        filter the query with the configured filters
        """
        for method in self._get_filters():
            query = method(query, appstruct)
        return query

    def _get_sort_key(self, appstruct):
        """
        Retrieve the sort key to use

        :param dict appstruct: Form submitted datas
        :rtype: str
        """
        if 'sort' in self.request.GET:
            result = self.request.GET['sort']
        elif 'sort' in appstruct:
            result = appstruct['sort']
        else:
            result = self.default_sort
        return result

    def _get_sort_direction(self, appstruct):
        """
        Retrieve the sort direction to use

        :param dict appstruct: Form submitted datas
        :rtype: str
        """
        if 'direction' in self.request.GET:
            result = self.request.GET['direction']
        elif 'direction' in appstruct:
            result = appstruct['direction']
        else:
            result = self.default_direction
        return result

    def _sort(self, query, appstruct):
        """
        Sort the results regarding the default values and
        the sort_columns dict, maybe overriden to provide a custom sort
        method
        """
        sort_column_key = self._get_sort_key(appstruct)
        self.logger.debug("  + Sorting the query : %s" % sort_column_key)
        sort_column = self.sort_columns.get(sort_column_key)

        if sort_column:
            sort_direction = self._get_sort_direction(appstruct)
            self.logger.debug("  + Direction : %s" % sort_direction)

            if sort_direction == 'asc':
                func = asc
                query = query.order_by(func(sort_column))
            elif sort_direction == 'desc':
                func = desc
                query = query.order_by(func(sort_column))
        return query

    def set_form_widget(self, form):
        """
        Attach a custom widget to the given form

        :param obj form: The deform.Form instance
        :returns: The deform.Form instance
        :rtype: obj
        """
        if self.grid is not None:
            form.formid = 'grid_search_form'
            form.widget = deform_extensions.GridFormWidget(
                named_grid=self.grid
            )
        else:
            form.widget.template = "searchform.pt"
        return form

    def get_filter_button(self):
        """
        Return the definition of the filter button
        """
        self.logger.debug(
            "Building the filter button : %s" % self.filter_button_label
        )
        return deform.Button(
            title=self.filter_button_label,
            name='submit',
            type='submit',
            css_class='btn btn-primary'
        )

    def get_form(self, schema):
        """
        Return the search form that should be used for this view

        :param obj schema: The form's colander.Schema
        :returns: The form object
        :rtype: obj
        """
        # counter is used to avoid field name conflicts
        form = Form(
            schema,
            counter=itertools.count(15000),
            method='GET'
        )
        form = self.set_form_widget(form)
        form.buttons = (self.get_filter_button(), )
        return form

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
                form = self.get_form(schema)
                if '__formid__' in self.request.GET:
                    submitted = self.request.GET.items()
                    appstruct = form.validate(submitted)
                else:
                    appstruct = form.cstruct
            except deform.ValidationFailure as e:
                # If values are not valid, we want the default ones to be
                # provided see the schema definition
                self.logger.exception("  - Current search values are not valid")
                self.logger.error(e)
                if hasattr(e, 'error'):
                    self.logger.error(e.error)
                appstruct = schema.deserialize({})
                self.error = e

        return schema, appstruct

    def __call__(self):
        self.logger.debug(u"# Calling the list view #")
        self.logger.debug(u" + Collecting the appstruct from submitted datas")
        schema, appstruct = self._collect_appstruct()
        self.appstruct = appstruct
        self.logger.debug(appstruct)
        self.logger.debug(u" + Launching query")
        query = self.query()
        if query is not None:
            self.logger.debug(u" + Filtering query")
            query = self._filter(query, appstruct)
            self.logger.debug(u" + Sorting query")
            query = self._sort(query, appstruct)

        self.logger.debug(u" + Building the return values")
        return self._build_return_value(schema, appstruct, query)

    def _build_return_value(self, schema, appstruct, query):
        """
        To be implemented : datas returned by the view
        """
        return {}


def get_page_url(request, page):
    """
    Page url generator to be used with webob.paginate's tool

    Note : default Webob pagination tool doesn't respect query_params order and
    breaks mapping order, so we can't preserve search params in list views
    """
    args = request.GET.copy()
    args['page'] = str(page)
    return request.current_route_path(_query=args)


class PopupMixin(object):
    """
    Provide methods for handling popup related actions
    """

    def add_popup_response(self):
        """
        Add custom response string to the request :
            Pop message
            or
            Refresh parent page

        regarding the options
        if
        a message was set in the queue, it's shown with a refresh link
        else
        we fully reload the page

        """
        self.logger.debug("Building a popup_close response")
        msg = self.request.session.pop_flash(queue="")
        if msg:
            set_close_popup_response(
                self.request,
                msg[0],
            )
        else:
            set_close_popup_response(self.request, force_reload=True)


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
    add_template_vars = ()
    grid = None
    use_paginate = True

    def _get_item_url(self, item, action=None, **kw):
        """
        Build an url to an item's action

        Usefull from inside the stream_actions method

        :param obj item: An instance with an id
        :param str action: The name of the action
        (duplicate/disable/edit...)
        :param dict kw: Other optionnal route params passed to route_path call

        :returns: An url
        :rtype: str
        """
        if not hasattr(self, 'item_route_name'):
            raise Exception(u"Un attribut item_route_name doit être défini")

        query = dict(self.request.GET)
        if action is not None:
            query['action'] = action

        return self.request.route_path(
            self.item_route_name,
            id=item.id,
            _query=query,
            **kw
        )

    def _get_current_page(self, appstruct):
        """
        Return the current requested page
        """
        if 'page' in self.request.GET:
            res = self.request.GET['page']
        elif 'page' in appstruct:
            res = appstruct['page']
        else:
            res = 1
        return convert_to_int(res)

    def _paginate(self, query, appstruct):
        """
            wraps the current SQLA query with pagination
        """
        if self.use_paginate:
            # Url builder for page links
            from functools import partial
            page_url = partial(get_page_url, request=self.request)

            current_page = self._get_current_page(appstruct)
            items_per_page = convert_to_int(appstruct.get('items_per_page', 30))

            self.logger.debug(
                " + Page : %s, items per page : %s" % (
                    current_page, items_per_page
                )
            )
            self.logger.debug(query)
            page = paginate.Page(
                query,
                current_page,
                url=page_url,
                items_per_page=items_per_page
            )
            self.logger.debug(page)
            return page
        else:
            return query

    def more_template_vars(self, response_dict):
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
        if query is None:
            records = None
        else:
            if self.use_paginate:
                records = self._paginate(query, appstruct)
            else:
                records = query

        result = dict(records=records, use_paginate=self.use_paginate)

        if schema is not None:
            if self.error is not None:
                result['form_object'] = self.error
                result['form'] = self.error.render()
            else:
                form = self.get_form(schema)
                if appstruct and '__formid__' in self.request.GET:
                    form.set_appstruct(appstruct)
                result['form_object'] = form
                result['form'] = form.render()

        result['title'] = self.title
        result.update(self.more_template_vars(result))
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
        self.logger.debug(u"# Initializing a writer %s" % self.writer)
        self.logger.debug(u" + For the model : %s" % self.model)
        writer = self.writer(model=self.model)
        if hasattr(self, 'sheet_title') and hasattr(writer, 'set_title'):
            writer.set_title(self.sheet_title)
        return writer

    def _build_return_value(self, schema, appstruct, query):
        """
        Return the streamed file object
        """
        writer = self._init_writer()
        self.logger.debug(u" + Streaming rows")
        for item in self._stream_rows(query):
            writer.add_row(item)
        self.logger.debug(u" + Writing the file to the request")
        write_file_to_request(self.request, self.filename, writer.render())
        return self.request.response


class BaseXlsView(BaseCsvView):
    writer = SqlaXlsExporter


class BaseOdsView(BaseCsvView):
    writer = SqlaOdsExporter


class BaseFormView(FormView, PopupMixin):
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
    use_csrf_token = False

    def __init__(self, context, request=None):
        if request is None:
            # Needed for manually called views
            self.request = context
            self.context = self.request.context
        else:
            self.request = request
            self.context = context
        FormView.__init__(self, self.request)
        self.dbsession = self.request.dbsession
        self.session = self.request.session
        self.logger = logging.getLogger("autonomie.views.__init__")
        if self.request.has_permission('manage'):
            tinymce.need()

    def before(self, form):
        FormView.before(self, form)
        if hasattr(self, "named_form_grid"):
            form.widget = GridFormWidget(named_grid=self.named_form_grid)
        elif hasattr(self, 'form_grid'):
            form.widget = GridFormWidget(grid=self.form_grid)

    def __call__(self):
        if self.use_csrf_token and 'csrf_token' not in self.schema:
            self.schema.children.append(CSRFSchema()['csrf_token'])
        try:
            result = FormView.__call__(self)
        except colander.Invalid, exc:
            self.logger.exception(
                "Exception while rendering form "
                "'%s': %s - struct received: %s",
                self.title, exc, self.appstruct())
            raise
        if isinstance(result, dict):
            result.update(self._more_template_vars())

        if self.request.is_popup:
            if isinstance(result, HTTPFound):
                self.add_popup_response()
                return self.request.response
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
        form = self.form_class(
            self.schema,
            buttons=self.buttons,
            use_ajax=use_ajax,
            ajax_options=ajax_options,
            **dict(self.form_options)
        )
        self.before(form)
        return form

    def submit_failure(self, e):
        """
        Called by default when we failed to submit the values
        We add a token here for forms that are collapsed by default to keep them
        open if there is an error
        """
        self.logger.exception(e)
        # On loggergue l'erreur colander d'origine
        self.logger.exception(e.error)
        print(e)
        print(e.error)
        return dict(form=e.render(), formerror=True)


class BaseAddView(BaseFormView):
    """
    Admin view that should be subclassed adding a colanderalchemy schema

    class AdminModel(BaseAddView):
        schema = SQLAlchemySchemaNode(MyModel)
        model = MyModel
    """
    add_template_vars = ('title', 'help_msg')
    msg = u"Vos modifications ont bien été enregistrées"
    factory = None
    redirect_route = None

    @property
    def help_msg(self):
        factory = getattr(self, 'factory', None)
        if factory is not None:
            calchemy_dict = getattr(factory, '__colanderalchemy_config__', {})
        else:
            calchemy_dict = {}
        return calchemy_dict.get('help_msg', '')

    def create_instance(self):
        """
        Initiate a new instance
        """
        if self.factory is None:
            raise Exception("Missing mandatory 'factory' attribute")
        return self.factory()

    def merge_appstruct(self, appstruct, model):
        """
        Merge the appstruct with the newly create model

        :param dict appstruct: Validated form datas
        :param obj model: A new instance of the object we create
        :returns: The model this view is supposed to add
        """
        model = self.schema.objectify(appstruct, model)
        return model

    def submit_success(self, appstruct):
        new_model = self.create_instance()
        new_model = self.merge_appstruct(appstruct, new_model)
        self.dbsession.add(new_model)

        if hasattr(self, 'on_add'):
            self.on_add(new_model, appstruct)

        self.dbsession.flush()
        if self.msg:
            self.request.session.flash(self.msg)

        if hasattr(self, 'redirect'):
            return self.redirect(new_model)
        elif self.redirect_route is not None:
            return HTTPFound(self.request.route_path(self.redirect_route))


class BaseEditView(BaseFormView):
    """
    ColanderAlchemy schema based view

    class AdminModel(BaseEditView):
        schema = SQLAlchemySchemaNode(MyModel)
    """
    add_template_vars = ('title', 'help_msg')
    msg = u"Vos modifications ont bien été enregistrées"
    redirect_route = None

    @property
    def help_msg(self):
        factory = getattr(self, 'factory', None)
        if factory is not None:
            calchemy_dict = getattr(factory, '__colanderalchemy_config__', {})
        else:
            calchemy_dict = {}
        return calchemy_dict.get('help_msg', '')

    def get_default_appstruct(self):
        """
        Collect datas that will initially populate the form
        """
        model = self.get_context_model()
        return self.schema.dictify(model)

    def before(self, form):
        BaseFormView.before(self, form)
        form.set_appstruct(self.get_default_appstruct())

    def merge_appstruct(self, appstruct, model):
        """
        Merge the appstruct with the newly create model

        :param dict appstruct: Validated form datas
        :param obj model: A new instance of the object we create
        :returns: The model this view is supposed to add
        """
        model = self.schema.objectify(appstruct, model)
        return model

    def get_context_model(self):
        """
        Return the model we're editing, by default it's the current context but
        in case of OneToOne relationship, it can be that the context is a
        related model, Overriding this method we can provide the model to edit

        :returns: The model that will be edited by this view
        """
        return self.context

    def submit_success(self, appstruct):
        model = self.get_context_model()
        model = self.merge_appstruct(appstruct, model)
        self.dbsession.merge(model)

        if hasattr(self, 'on_edit'):
            self.on_edit(appstruct)

        self.dbsession.flush()
        if self.msg:
            self.request.session.flash(self.msg)

        if hasattr(self, 'redirect'):
            return self.redirect()
        elif self.redirect_route is not None:
            return HTTPFound(self.request.route_path(self.redirect_route))
        else:
            raise Exception("A redirection strategy should be provided")

    def cancel_success(self, appstruct):
        if hasattr(self, 'redirect'):
            return self.redirect()
        elif self.redirect_route is not None:
            return HTTPFound(self.request.route_path(self.redirect_route))
        else:
            raise Exception("A redirection strategy should be provided")


class DisableView(BaseView):
    """
    Main view for enabling/disabling elements

    Support following attributes/methods

    Attributes

        enable_msg

                Message flashed when enabled

        disable_msg

                Message flashed when disabled

        redirect_route

                The name of a route to redirect to

    Methods

        redirect

            Return a dynamicallay created HTTPFound instance

        on_disable

            Launched on item disable

        on_enable

            Launched on item enable


    class MyDisableView(DisableView):
        enable_msg = u"Has been enabled"
        disabled_msg = u"Has been disabled"
        redirect_route = u"The route name"
    """
    enable_msg = None
    disable_msg = None
    redirect_route = None

    def __call__(self):
        if self.context.active:
            self.context.active = False
            self.request.dbsession.merge(self.context)
            if hasattr(self, "on_disable"):
                self.on_disable()

            if self.disable_msg is not None:
                self.request.session.flash(self.disable_msg)
        else:
            self.context.active = True
            self.request.dbsession.merge(self.context)
            if hasattr(self, "on_enable"):
                self.on_enable()
            if self.enable_msg is not None:
                self.request.session.flash(self.enable_msg)

        if hasattr(self, 'redirect'):
            return self.redirect()
        elif self.redirect_route is not None:
            return HTTPFound(self.request.route_path(self.redirect_route))


class DeleteView(BaseView, PopupMixin):
    """
    main deletion view

    class MyDeleteView(DeleteView):
        delete_msg = u"L'élément a bien été supprimé"
        redirect_route = "templates"

    """
    delete_msg = u"L'élément a bien été supprimé"
    redirect_route = None

    def __call__(self):
        if hasattr(self, "on_before_delete"):
            self.on_before_delete()
        self.request.dbsession.delete(self.context)
        self.request.session.flash(self.delete_msg)

        if hasattr(self, "on_delete"):
            self.on_delete()

        if hasattr(self, 'redirect'):
            result = self.redirect()
        elif self.redirect_route is not None:
            result = HTTPFound(self.request.route_path(self.redirect_route))

        if self.request.is_popup:
            if isinstance(result, HTTPFound):
                self.add_popup_response()
                return self.request.response
        return result


class DuplicateView(BaseView):
    """
    Base Duplication view

    calls the duplicate method on the view's context
    flash a link to the duplicated item
    redirect to the redirect route

    :attr str route_name: The route_name used to generate the link to the
    duplication view (implement _link to override default generation)

    :attr str collection_route_name: optionnal collection route name to which
    redirect (default set to route_name + 's'), implement a _redirect method to
    override the redirection mechanism

    :attr str message: The duplication message, take a single formatting value
    (the link to the new item)
    """
    message = None
    route_name = None
    collection_route_name = None

    def _link(self, item):
        if self.route_name is None:
            raise Exception("Set a route_name attribute for link generation")
        return self.request.route_path(self.route_name, id=item.id)

    def _message(self, item):
        if self.message is None:
            raise Exception("Set a message attribute for flashed message \
generation")
        return self.message.format(self._link(item))

    def redirect(self, item):
        """
        Default redirect implementation

        :param obj item: The newly created element (flushed)
        :returns: The url to redirect to
        :rtype: str
        """
        return HTTPFound(
            self.request.route_path(self.route_name, id=item.id)
        )

    def __call__(self):
        item = self.context.duplicate()
        self.request.dbsession.add(item)
        # We need an id
        self.request.dbsession.flush()
        if hasattr(self, "on_duplicate"):
            self.on_duplicate(item)

        self.request.session.flash(self._message(item))
        return self.redirect(item)


class BaseRestView(BaseView):
    """
    A base rest view

    provides the base structure for a rest view for sqlalchemy model access

    it handles :

        get
        delete
        put
        post requests

    thanks to the colanderalchemy tools, we dynamically build the resulting
    model

    Following datas should be provided :

        * Attributes

            schema

                A colanderalchemy schema, it can be provided through a property
                or a simple attribute. For on the fly schema handling, you can
                also override the get_schema method that returns self.schema by
                default

    The following could be provided

        Methods

            get_schema

                See above comment

            pre_format

                Preformat submitted values before passing them to the form
                schema

            post_format

                PostFormat the generated (or modified) model and launch some
                custom action

    """
    schema = None

    def get_schema(self, submitted):
        return self.schema

    def filter_edition_schema(self, schema, submitted):
        """
        filter the schema in case of edition removing all keys not present in
        the submitted datas (allow to edit only one field)

        :param dict submitted: the raw submitted datas
        :param obj schema: the schema we're going to use
        """
        # In edition, we only keep edited fields
        submitted_keys = submitted.keys()
        toremove = [
            node for node in schema if node.name not in submitted_keys
        ]
        self.logger.debug(u"Removing %s from the schema" % toremove)
        for node in toremove:
            del schema[node.name]

        return schema

    def get(self):
        return self.context

    def pre_format(self, datas):
        """
        Allows to apply pre-formatting to the submitted datas
        """
        return datas

    def post_format(self, entry, edit, attributes):
        """
        Allos to apply post formatting to the model before flushing it
        """
        return entry

    def get_editted_element(self, attributes):
        """
        Returns the element we edit
        """
        return self.context

    def _submit_datas(self, submitted, edit=False):
        self.logger.debug(u" + Submitting %s" % submitted)
        submitted = self.pre_format(submitted)
        self.logger.debug(u" + After pre format %s" % submitted)
        schema = self.get_schema(submitted)

        if edit:
            schema = self.filter_edition_schema(schema, submitted)

        schema = schema.bind(request=self.request)

        try:
            attributes = schema.deserialize(submitted)
        except colander.Invalid, err:
            self.logger.exception("  - Erreur")
            self.logger.exception(submitted)
            raise rest.RestError(err.asdict(), 400)

        self.logger.debug(u" + After deserialize : %s" % attributes)
        if edit:
            editted = self.get_editted_element(attributes)
            entry = schema.objectify(attributes, editted)
            entry = self.post_format(entry, edit, attributes)
            entry = self.request.dbsession.merge(entry)
        else:
            entry = schema.objectify(attributes)
            entry = self.post_format(entry, edit, attributes)
            self.request.dbsession.add(entry)
            # We need an id => flush
            self.request.dbsession.flush()
        self.logger.debug("Finished")
        return entry

    def post(self):
        self.logger.info("POST request")
        submitted = self.request.json_body
        return self._submit_datas(submitted, edit=False)

    def put(self):
        self.logger.info("PUT request")
        submitted = self.request.json_body
        return self._submit_datas(submitted, edit=True)

    def delete(self):
        """
        Delete the given entry
        """
        self.logger.info("DELETE request")
        self.request.dbsession.delete(self.context)
        return {}


class TreeMixinMetaClass(type):
    """
    Metaclasse qui attache un attribut children spécifique à chaque classe fille
    créée


    LE problème d'origine :

        class A:
            children = []

        class B(A):
            pass

        B.children.append('o')
        A.children
        ['o']

    Avec cette métaclasse

    A.children = []
    """
    def __new__(cls, clsname, bases, attrs):
        newclass = super(TreeMixinMetaClass, cls).__new__(
            cls, clsname, bases, attrs
        )
        newclass.children = []
        return newclass


class TreeMixin:
    """
    Mixin adding tree structure to views

    class MyView(BaseView, TreeMixin):
        route_name = "/myviewroute"


    Inherit from the TreeMixin and attach views to parent views

    route_name

        current route_name

    children

        class attribute in list format registering all view children

    parent

        weakref to the parent view
    """
    __metaclass__ = TreeMixinMetaClass
    route_name = None
    parent_view = None
    description = ""
    title = ""

    @classmethod
    def get_url(cls, request):
        if getattr(cls, 'url', None) is not None:
            return cls(request).url
        elif getattr(cls, 'route_name', None) is not None:
            if isinstance(cls.route_name, property):
                return cls(request).route_name
            else:
                return request.route_path(cls.route_name)
        else:
            return ""

    @classmethod
    def get_title(cls, request):
        if isinstance(cls.title, property):
            return cls(request).title
        else:
            return cls.title

    @classmethod
    def get_breadcrumb(cls, request, local=False):
        """
        Collect breadcrumb entries

        :param obj request: The Pyramid request
        :param bool local: Is the breadcrumb for local use
        :returns: A generator of 2-uples (title, url)
        """
        if cls.parent_view is not None:
            for link in cls.parent_view.get_breadcrumb(request):
                yield link

        if not local:
            yield Link(cls.get_url(request), cls.get_title(request))
        else:
            yield Link("", cls.get_title(request))

    @classmethod
    def get_back_url(cls, request):
        logger.debug(u"Asking for the parent url : {0}".format(cls))
        if cls.parent_view is not None:
            return cls.parent_view.get_url(request)
        else:
            return None

    @classmethod
    def get_navigation(cls, request):
        result = []
        for child in cls.children:
            if getattr(child, 'route_name', None) is not None:
                result.append(
                    Link(
                        label=child.title,
                        route_name=child.route_name,
                        title=child.description,
                    )
                )
            else:
                url = child.get_url(request)
                if url:
                    result.append(
                        Link(
                            label=child.title,
                            title=child.description,
                            url=url,
                        )
                    )
        return result

    @property
    def navigation(self):
        return self.get_navigation(self.request)

    @property
    def breadcrumb(self):
        return self.get_breadcrumb(self.request, local=True)

    @property
    def back_link(self):
        return self.get_back_url(self.request)

    @classmethod
    def add_child(cls, view_class):
        cls.children.append(view_class)
        view_class.parent_view = cls

    def populate_navigation(self):
        try:
            self.request.navigation.breadcrumb = self.breadcrumb
            self.request.navigation.back_link = self.back_link
        except Exception as err:
            logger.exception(u"Error in populate_navigation")
            logger.error(u"I'm %s " % self)
            logger.error(u"Parent : %s" % self.parent_view)
            raise err


def make_panel_wrapper_view(panel_name, js_resources=()):
    """
    Return a view wrapping the given panel

    :param str panel_name: The name of the panel
    """
    def myview(request):
        """
            Return a panel name for our panel wrapper
        """
        if js_resources:
            for js_resource in js_resources:
                js_resource.need()
        return {'panel_name': panel_name}
    return myview


def add_panel_view(config, panel_name, **kwargs):
    """
    Add a panel view to the current configuration
    """
    config.add_view(
        make_panel_wrapper_view(panel_name),
        renderer="panel_wrapper.mako",
        xhr=True,
        **kwargs
    )


def add_panel_page_view(config, panel_name, **kwargs):
    js_resources = kwargs.pop('js_resources', ())
    config.add_view(
        make_panel_wrapper_view(panel_name, js_resources),
        renderer="panel_page_wrapper.mako",
        **kwargs
    )


def add_tree_view_directive(config, *args, **kwargs):
    """
    Custom add view directive specific to views using the TreeMixin class
    It allows to pass a parent parameter matching the parent view

    This way views can display a breadcrumb for navigation
    """
    if 'parent' in kwargs:
        parent = kwargs.pop('parent')
        if not hasattr(parent, 'add_child'):
            raise Exception(u"The parent (%s) view should inherit the "
                            u"Treemixin class" % parent)
        parent.add_child(args[0])

    if 'route_name' not in kwargs:
        # Use the route_name set on the view by default
        kwargs['route_name'] = args[0].route_name

    config.add_view(*args, **kwargs)


def includeme(config):
    """
    Pyramid inclusion mechanism
    """
    config.add_directive('add_tree_view', add_tree_view_directive)
