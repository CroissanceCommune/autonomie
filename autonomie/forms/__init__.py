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
Main deferreds functions used in autonomie

The widgets provided here are model agnostic
"""
import colander
import datetime
import deform
import deform_extensions

from autonomie.utils import strings
from autonomie.utils.fileupload import FileTempStore
from autonomie.utils.html import (
    clean_html,
    strip_html,
)


EXCLUDED = {'exclude': True}
MAIL_ERROR_MESSAGE = u"Veuillez entrer une adresse e-mail valide"


@colander.deferred
def deferred_today(node, kw):
    """
        return a deferred value for "today"
    """
    return datetime.date.today()


@colander.deferred
def deferred_now(node, kw):
    """
    Return a deferred datetime value for now
    """
    return datetime.datetime.now()


@colander.deferred
def deferred_current_user_id(node, kw):
    """
        Return a deferred for the current user
    """
    return kw['request'].user.id


def get_date_input(**kw):
    """
    Return a date input displaying a french user friendly format
    """
    date_input = deform_extensions.CustomDateInputWidget(**kw)
    return date_input


def get_datetime_input(**kw):
    """
    Return a datetime input displaying a french user friendly format
    """
    datetime_input = deform_extensions.CustomDateTimeInputWidget(**kw)
    return datetime_input


def today_node(**kw):
    """
    Return a schema node for date selection, defaulted to today
    """
    if "default" not in kw:
        kw['default'] = deferred_today
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
        colander.Date(),
        widget=get_date_input(**widget_options),
        **kw
    )


def now_node(**kw):
    """
    Return a schema node for time selection, defaulted to "now"
    """
    if "default" not in kw:
        kw['default'] = deferred_now
    return colander.SchemaNode(
        colander.DateTime(default_tzinfo=None),
        widget=get_datetime_input(),
        **kw)


def come_from_node(**kw):
    """
    Return a form node for storing the come_from page url
    """
    if "missing" not in kw:
        kw["missing"] = ""
    return colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        **kw
    )


@colander.deferred
def deferred_default_popup(node, kw):
    """
    Check if the popup key is present in get or post params and return its id
    """
    return kw['request'].params.get('popup', '')


def popup_node(**kw):
    """
    Return a form node for storing the come_from page url
    """
    return colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        missing=colander.drop,
        default=deferred_default_popup
    )


def _textarea_node_validator(value):
    """
    Check that the given value is not void (it could contain void html tags)
    """
    return bool(strip_html(value))


textarea_node_validator = colander.Function(
    _textarea_node_validator,
    msg=u"Ce paramètre est requis"
)


def richtext_widget(options=None, widget_options=None, admin=False):
    """
    Return a text area widget
    """
    options = options or {}
    widget_options = widget_options or {}
    plugins = [
        "lists",
        "searchreplace visualblocks fullscreen",
        # "contextmenu paste"
    ]
    menubar = False
    if admin:
        plugins.append("insertdatetime searchreplace code table")
        plugins.append("advlist link autolink")
        menubar = True

    options.update({
        'content_css': "/fanstatic/fanstatic/css/richtext.css",
        'language': "fr_FR",
        'menubar': menubar,
        'plugins': plugins
    })

    return deform.widget.RichTextWidget(
        options=options.items(),
        **widget_options
    )


def textarea_node(**kw):
    """
    Return a node for storing Text objects

    richtext (True / False)

        should we provide a rich text widget if True, richtext_options dict
        values will be passed to the CKEditor library

    admin (True / False)

        Should we provide a widget with all options

    widget_options

        Options passed to the widget's class

    """
    widget_options = kw.pop('widget_options', {})

    if kw.pop('richwidget', None):
        # If the admin option is set,
        admin_field = kw.pop('admin', False)
        options = kw.pop("richtext_options", {})
        wid = richtext_widget(options, widget_options, admin=admin_field)
    else:
        widget_options.setdefault("rows", 4)
        wid = deform.widget.TextAreaWidget(**widget_options)

    kw.setdefault(
        'preparer',
        clean_html
    )
    return colander.SchemaNode(
        colander.String(),
        widget=wid,
        **kw
    )


@colander.deferred
def default_year(node, kw):
    return datetime.date.today().year


def get_year_select_deferred(query_func, default_val=None):
    """
    return a deferred widget for year selection
    :param query_func: the query function returning a list of years (taks kw as
    parameters)
    """
    @colander.deferred
    def deferred_widget(node, kw):
        years = query_func(kw)
        values = zip(years, years)
        if default_val is not None and default_val not in years:
            values.insert(0, default_val)

        return deform.widget.SelectWidget(
            values=values,
            css_class='input-small',
        )
    return deferred_widget


def year_select_node(query_func, **kw):
    """
    Return a year select node with defaults and missing values

    :param query_func: a function to call that return the years we want to
        display
    """
    title = kw.pop('title', u"")
    missing = kw.pop('missing', default_year)
    widget_options = kw.pop('widget_options', {})
    default_val = widget_options.get('default_val')
    return colander.SchemaNode(
        colander.Integer(),
        widget=get_year_select_deferred(query_func, default_val),
        default=default_year,
        missing=missing,
        title=title,
        **kw
    )


@colander.deferred
def default_month(node, kw):
    return datetime.date.today().month


def get_month_options():
    return [(index, strings.month_name(index)) for index in range(1, 13)]


def range_validator(appstruct):
    """
    Validate that start and end keys are in the good order (dates, amounts ...)

    :param dict appstruct: The validated datas containing a start and a
    end key
    """
    start = appstruct.get('start')
    if start is not None:
        end = appstruct.get('end')
        if end is not None:
            if end < start:
                return False
    return True


def get_month_select_widget(widget_options):
    """
    Return a select widget for month selection
    """
    options = get_month_options()
    default_val = widget_options.get('default_val')
    if default_val is not None:
        options.insert(0, default_val)
    return deform.widget.SelectWidget(values=options, css_class='input-small')


def month_select_node(**kw):
    """
    Return a select widget for month selection
    """
    title = kw.pop('title', u"")
    default = kw.pop('default', default_month)
    missing = kw.pop('missing', default_month)
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
        colander.Integer(),
        widget=get_month_select_widget(widget_options),
        default=default,
        missing=missing,
        title=title,
        **kw
    )


def mail_validator():
    """
    Return an email entry validator with a custom error message
    """
    return colander.Email(MAIL_ERROR_MESSAGE)


def mail_node(**kw):
    """
        Return a generic customized mail input field
    """
    title = kw.pop('title', None) or u"Adresse e-mail"
    return colander.SchemaNode(
        colander.String(),
        title=title,
        validator=mail_validator(),
        **kw)


def id_node():
    """
    Return a node for id recording (usefull in edition forms for retrieving
    original objects)
    """
    return colander.SchemaNode(
        colander.Integer(),
        widget=deform.widget.HiddenWidget(),
        missing=colander.drop,
        )


def get_fileupload_widget(store_url, store_path, session,
                          default_filename=None, filters=None):
    """
        return a file upload widget
    """
    tmpstore = FileTempStore(
        session,
        store_path,
        store_url,
        default_filename=default_filename,
        filters=filters,
    )
    return deform.widget.FileUploadWidget(
        tmpstore,
        template="fileupload.pt"
    )


def public_file_appstruct(request, config_key, file_object):
    """
    Build a form appstruct suitable for a colander File Node from a ConfigFile
    instance

    :param obj request: The Pyramid request
    :param str config_key: The config key under which the file is stored :param
    obj file_object: A :class:`autonomie.models.files.ConfigFile` instance
    :rtype: dict
    """
    if file_object is None:
        raise Exception("file_appstruct should not be called with a None "
                        u"file object")
    else:
        return {
            "uid": file_object.id,
            "filename": file_object.name,
            "preview_url": request.route_path(
                "public",
                name=config_key
            )
        }


def file_appstruct(request, file_id):
    """
    Build a form appstruct suitable for a colander File Node from a File
    instance

    :param obj request: The Pyramid request
    :param int file_id: The id of a :class:`autonomie.models.files.File`
    instance
    :rtype: dict
    """
    if file_id is None:
        raise Exception("file_appstruct should not be called with a None "
                        u"file object")
    else:
        return {
            "uid": file_id,
            "filename": u"%s.png" % file_id,
            "preview_url": request.route_path(
                "filepng",
                id=file_id
            )
        }


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


def merge_session_with_post(model, app_struct, remove_empty_values=True):
    """
        Merge Deform validated datas with SQLAlchemy's objects
        Allow to spare some lines of assigning datas to the object
        before writing to database

        model

            The sqlalchemy model

        app_struct

            The datas retrieved for example from a form

        remove_empty_values

            should we remove the colander.null / None values or set them
            on model.
    """
    for key, value in app_struct.items():
        if value == colander.null:
            value = None
        if not (remove_empty_values and value is None):
            setattr(model, key, value)
    return model


def get_excluded(title=None):
    """
    Return a colanderalchemy info dict for excluded columns (includes a title
    for other sqla inspection tools like sqla_inspect library)
    """
    res = {'exclude': True}
    if title is not None:
        res['title'] = title
    return res


def get_hidden_field_conf(title=None):
    """
    Return the model's info conf to get a colanderalchemy hidden widget
    """
    res = {
        'widget': deform.widget.HiddenWidget(),
        'missing': None
    }
    if title is not None:
        res['title'] = title
    return res


def get_deferred_model_select_validator(model, id_key='id', filters=[]):
    """
    Return a deferred validator based on the given model

        model

            Option model having at least two attributes id and label

        id_key

            The model attr used to store the related object in db (mostly id)

        filters

            list of 2-uples allowing to filter the model query
            (attr/value)
    """
    @colander.deferred
    def deferred_validator(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        query = model.query()
        for key, value in filters:
            query = query.filter(getattr(model, key) == value)

        return colander.OneOf([getattr(m, id_key) for m in query])
    return deferred_validator


get_deferred_select_validator = get_deferred_model_select_validator


def get_model_select_option_values(
    model, keys, filters=(), add_default=True, empty_filter_msg=''
):
    """
    Build an option list that can be used by SelectWidget and CheckboxListWidget

    :param obj model: The model to query
    :param tuple keys: A 2-uple (idkey, labelkey) to query on the model (it's
    possible to pass callables getting the model as only argument)
    :param list filters: List of 2-uples (key, value)
    :param bool add_default: Should we add a default void value
    :returns: a list of 2-uples
    """
    key1, key2 = keys

    values = []
    if add_default or empty_filter_msg:
        values.append(('', empty_filter_msg))

    query = model.query()
    for key, value in filters:
        query = query.filter(getattr(model, key) == value)

    for instance in query:
        if callable(key1):
            key = key1(instance)
        else:
            key = getattr(instance, key1)

        if callable(key2):
            label = key2(instance)
        else:
            label = getattr(instance, key2)
        values.append((key, label))
    return values


def get_deferred_model_select(
    model, multi=False, mandatory=False, keys=('id', 'label'), filters=[],
    empty_filter_msg="",
):
    """
    Return a deferred select widget based on the given model

        model

            Option model having at least two attributes id and label

        multi

            Should it support multiple item selection

        mandatory

            Is it a mandatory entry, if not, we insert a void value
            default: False

        keys

            a 2-uple describing the (value, label) of the select's options

        filters

            list of 2-uples allowing to filter the model query
            (attr/value)
    """
    @colander.deferred
    def deferred_widget(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        values = get_model_select_option_values(
            model,
            keys,
            filters,
            add_default=not mandatory,
            empty_filter_msg=empty_filter_msg,
        )
        return deform.widget.SelectWidget(values=values, multi=multi)
    return deferred_widget


get_deferred_select = get_deferred_model_select


def get_deferred_model_select_checkbox(
    model, keys=('id', 'label'), filters=[], widget_options={}
):
    """
    Return a deferred select widget based on the given model

        model

            Option model having at least two attributes id and label

        keys

            a 2-uple describing the (value, label) of the select's options

        filters

            list of 2-uples allowing to filter the model query
            (attr/value)

        widget_options

            deform widget options
    """
    @colander.deferred
    def deferred_widget(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        values = get_model_select_option_values(
            model, keys, filters, add_default=False
        )
        return deform.widget.CheckboxChoiceWidget(
            values=values,
            **widget_options
        )
    return deferred_widget


def get_deferred_default(model, default_key='default', id_key='id'):
    """
    Return a deferred for default model selection

        model

            Option model having at least an id and a default attribute

        default_key

            A boolean attr defining which element is the default one

        id_key

            The default value attr
    """
    @colander.deferred
    def deferred_default(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        default = model.query().filter(getattr(model, default_key)).first()
        if default is not None:
            return getattr(default, id_key)
        else:
            return colander.null
    return deferred_default


def get_select(values, multi=False, mandatory=True):
    """
    Return a select widget with the provided options

         values

            options as expected by the deform select widget (a sequence of
            2-uples: (id, label))
    """
    if not isinstance(values, list):
        values = list(values)
    if not mandatory:
        values.insert(0, ('', ''))
    return deform.widget.SelectWidget(values=values, multi=False)


def get_select_validator(options):
    """
    return a validator for the given options

        options

            options as expected by the deform select widget (a sequence of
            2-uples : (id, label))

    """
    return colander.OneOf([o[0] for o in options])


def get_radio(values, mandatory=True, **kw):
    """
    Return a radio widget with the provided options

         values

            options as expected by the deform select widget (a sequence of
            2-uples: (id, label))
    """
    if not isinstance(values, list):
        values = list(values)
    if not mandatory:
        values.insert(0, ('', ''))
    return deform.widget.RadioChoiceWidget(values=values, **kw)


positive_validator = colander.Range(
    min=0,
    min_err=u"Doit être positif",
)
negative_validator = colander.Range(
    max=0,
    min_err=u"Doit être négatif",
)


class CustomModelSchemaNode(colander.SchemaNode):
    """
    Using colanderalchemy, it generates a schema regarding a given model, for
    relationships, it provides a schema for adding related datas.  We want to
    be able to configure relationships to existing datas (for example to
    configurable options)

    This SchemaNode subclass provides the methods expected in colanderalchemy
    for serialization/deserialization, it allows us to insert custom schemanode
    in colanderalchemy SQLAlchemySchemaNode
    """
    def dictify(self, instance):
        """
        Return the datas needed to fill the form
        """
        return getattr(instance, self.name)

    def objectify(self, value):
        """
        Return the related object that have been configured
        """
        from autonomie_base.models.base import DBSESSION
        res = DBSESSION().query(self.model).filter(
            getattr(self.model, self.name) == value
        ).first()
        if res is None:
            res = colander.null
        return res


def get_sequence_child_item_id_node(model, **kw):
    """
    Build a child item SchemaNode compatible with colanderalchemy's
    serialization technic it provides a node with dictify and objectify methods

    It can be used when editing M2M or O2M relationships

    :param obj model: The model we relay
    """
    if 'name' not in kw:
        kw['name'] = 'id'

    return CustomModelSchemaNode(
        colander.Integer(),
        model=model,
        **kw
    )


def get_sequence_child_item(
    model, required=False, child_attrs=('id', 'label'),
):
    """
    Return the schema node to be used for sequence of related elements
    configuration

    Usefull in a many to many or one to many relationships.
    Needed to be able to configure a sequence of relations to existing objects

    e.g:

        ICPE_codes = relationship(
            "ICPECode",
            secondary=ICPE_CODE_ASSOCIATION_TABLE,
            info={
                'colanderalchemy':{
                    'title': _(u"Code(s) ICPE"),
                    'children': forms.get_sequence_child_item(model)
                }
            },
            backref="company_info",
        )

    :param obj model: The model used for child items
    :param bool required: At least one element is required ?
    :param tuple child_attrs: The child attributes used to build the options in
    the form ('id_attr', 'label_attr') in most cases id_attr is used as foreign
    key and label_attr is the model's attribute used for display
    """
    missing = colander.drop
    if required:
        missing = colander.required

    return [
        get_sequence_child_item_id_node(
            widget=get_deferred_model_select(model, keys=child_attrs),
            missing=missing,
            model=model,
            validator=get_deferred_model_select_validator(model)
        )
    ]


class CustomModelSequenceSchemaNode(colander.SchemaNode):
    def __init__(self, *args, **kw):
        colander.SchemaNode.__init__(self, *args, **kw)

    def dictify(self, values):
        return [val.id for val in values]

    def objectify(self, ids):
        from autonomie_base.models.base import DBSESSION
        return DBSESSION().query(self.model).filter(
            self.model.id.in_(ids)
        ).all()


def get_model_checkbox_list_node(
    model, model_attrs=('id', 'label'), filters=[], **kw
):
    """
    Build a colander node representing a list of items presented in a checkbox
    list
    """
    widget_options = kw.pop('widget_options', {})
    return CustomModelSequenceSchemaNode(
        colander.Set(),
        model=model,
        widget=get_deferred_model_select_checkbox(
            model, keys=model_attrs, filters=filters,
            widget_options=widget_options
        ),
        **kw
    )


def customize_field(schema, field_name, widget=None, validator=None, **kw):
    """
    Customize a form schema field

    :param obj schema: the colander form schema
    :param str field_name: The name of the field to customize
    :param obj widget: a custom widget
    :param obj validator: A custom validator
    :param dict kw: Keyword args set as attributes on the schema field

    """
    if field_name in schema:
        if widget is not None:
            schema[field_name].widget = widget

        if validator is not None:
            schema[field_name].validator = validator

        for attr, value in kw.items():
            setattr(schema[field_name], attr, value)
    return schema


def reorder_schema(schema, child_order):
    """
    reorder a schema folowing the child_order

    :param obj schema: The colander schema :class:`colander.Schema`
    :param tuple child_order: The children order
    :returns: The schema
    :rtype: :class:`colander.Schema`
    """
    schema.children = [schema[node_name] for node_name in child_order]
    return schema


def mk_choice_node_factory(base_node_factory, resource_name, **parent_kw):
    """
    Specialize a node factory using Select2Widget
    to an item chooser among a list of items.

    Typical use:  field in add/edit form (think ForeignKey)

    :param function base_node_factory: a base node factory
    :param resource_name str: the name of the resource to be selected
      (used in widget strings and as default title)
    """
    def choice_node(**kw):
        # if a keyword is defined in both parent call and choice_node call,
        # priorize choice_node call (more specific).
        for k, v in parent_kw.items():
            kw.setdefault(k, v)

        widget_options = {
            'title': kw.get('title', resource_name),
            'placeholder': u"- Sélectionner {} -".format(resource_name),
            'default_option': ('', ''),  # required by placeholder
        }
        widget_options.update(kw.pop('widget_options', {}))
        return base_node_factory(
            widget_options=widget_options,
            **kw
        )
    return choice_node


def mk_filter_node_factory(base_node_factory, empty_filter_msg, **parent_kw):
    """
    Specialize a a node factory using Select2Widget
    to a list filtering node factory.

    :param function base_node_factory: a base node factory
    :param empty_filter_msg str: the name of the list item for "no filter"
      (used in widget strings)
    """
    def filter_node(**kw):
        for k, v in parent_kw.items():
            kw.setdefault(k, v)
        widget_options = {'default_option': ('', empty_filter_msg)}
        widget_options.update(kw.pop('widget_options', {}))

        return base_node_factory(
            missing=colander.drop,
            widget_options=widget_options,
            **kw
        )
    return filter_node
