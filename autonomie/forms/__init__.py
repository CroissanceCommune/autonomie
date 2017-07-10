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
import calendar
import datetime
import deform
import deform_extensions

from autonomie.utils.fileupload import FileTempStore
from autonomie.utils.html import (
    clean_html,
    strip_html,
)


TEMPLATES_PATH = "autonomie:deform_templates/"
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


def _textarea_node_validator(value):
    """
    Check that the given value is not void (it could contain void html tags)
    """
    return bool(strip_html(value))


textarea_node_validator = colander.Function(
    _textarea_node_validator,
    msg=u"Ce paramètre est requis"
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

        plugins = [
            "lists",
            "searchreplace visualblocks fullscreen",
            # "contextmenu paste"
        ]
        menubar = False
        if admin_field:
            plugins.append("insertdatetime searchreplace code table")
            plugins.append("advlist link autolink")
            menubar = True

        options = kw.pop("richtext_options", {})
        options.update({
            'content_css': "/fanstatic/fanstatic/css/richtext.css",
            'language': "fr_FR",
            'menubar': menubar,
            'plugins': plugins
        })

        wid = deform.widget.RichTextWidget(
            options=options.items(),
            **widget_options
        )
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
    :param query_func: the query function returning a list of years
    """
    @colander.deferred
    def deferred_widget(node, kw):
        years = query_func()
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
    return [(index, calendar.month_name[index].decode('utf8'))
            for index in range(1, 13)]


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
        template=TEMPLATES_PATH + "fileupload.pt"
    )


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


def merge_session_with_post(model, app_struct):
    """
        Merge Deform validated datas with SQLAlchemy's objects
        Allow to spare some lines of assigning datas to the object
        before writing to database

        model

            The sqlalchemy model

        app_struct

            The datas retrieved for example from a form
    """
    for key, value in app_struct.items():
        if value not in (None, colander.null,):
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


def get_deferred_select_validator(model, id_key='id'):
    """
    Return a deferred validator based on the given model

        model

            Option model having at least two attributes id and label

        id_key

            The model attr used to store the related object in db (mostly id)
    """
    @colander.deferred
    def deferred_validator(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        def my_custom_validator(node, value):
            key_val = value
            if isinstance(value, dict):
                key_val = value[id_key]
            elif isinstance(value, model):
                key_val = getattr(value, id_key)
            if key_val not in [getattr(m, id_key) for m in model.query()]:
                raise colander.Invalid(
                    node,
                    u"La valeur soumise ne fait pas partie des valeurs "
                    u"proposées"
                )
        return my_custom_validator
    return deferred_validator


def get_deferred_select(model, multi=False, mandatory=False,
                        keys=('id', 'label')):
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
    """
    @colander.deferred
    def deferred_widget(binding_datas, request):
        """
        The deferred function that will be fired on schema binding
        """
        key1, key2 = keys

        values = [(getattr(m, key1), getattr(m, key2)) for m in model.query()]
        if not mandatory:
            values.insert(0, ('', ''))
        return deform.widget.SelectWidget(values=values, multi=multi)
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


class CustomSchemaNode(colander.SchemaNode):
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
        return instance.id

    def objectify(self, id):
        """
        Return the related object that have been configured
        """
        from autonomie_base.models.base import DBSESSION
        return DBSESSION().query(self.model).get(id)


def get_sequence_child_item(
    model, label_attr='title', required=False
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
    """
    missing = colander.drop
    if required:
        missing = colander.required

    return [
        CustomSchemaNode(
            colander.Integer(),
            name='id',
            widget=get_deferred_select(model),
            missing=missing,
            model=model,
            validator=get_deferred_select_validator(model)
        )
    ]
