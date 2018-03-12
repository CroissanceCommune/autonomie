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
import logging
import colander

from sqlalchemy import desc
from pyramid.httpexceptions import (
    HTTPClientError,
)
from colanderalchemy import SQLAlchemySchemaNode
from sqla_inspect import csv

from autonomie.statistics import inspect

from autonomie.resources import statistics_js
from autonomie.models.user.userdatas import UserDatas
from autonomie.models.statistics import (
    StatisticSheet,
    StatisticEntry,
    BaseStatisticCriterion,
    CommonStatisticCriterion,
    OptListStatisticCriterion,
    DateStatisticCriterion,
    BoolStatisticCriterion,
    AndStatisticCriterion,
    OrStatisticCriterion,
)
from autonomie.statistics import (
    EntryQueryFactory,
    SheetQueryFactory,
    STRING_OPTIONS,
    BOOL_OPTIONS,
    NUMERIC_OPTIONS,
    OPTREL_OPTIONS,
    DATE_OPTIONS,
    MULTIDATE_OPTIONS,
)
from autonomie.utils import (
    widgets,
)
from autonomie_base.utils import ascii
from autonomie import forms
from autonomie.views import (
    BaseView,
    DisableView,
    DeleteView,
    DuplicateView,
    BaseRestView,
)
from autonomie.views.userdatas.lists import UserDatasCsvView
from autonomie.export.utils import write_file_to_request


CRITERION_MODELS = {
    "date": DateStatisticCriterion,
    "multidate": DateStatisticCriterion,
    "bool": BoolStatisticCriterion,
    "number": CommonStatisticCriterion,
    "optrel": OptListStatisticCriterion,
    "static_opt": OptListStatisticCriterion,
    "string": CommonStatisticCriterion,
    "or": OrStatisticCriterion,
    "and": AndStatisticCriterion,
}

logger = logging.getLogger(__name__)


def get_inspector(model=UserDatas):
    """
    Return a statistic inspector for the given model
    """
    return inspect.StatisticInspector(
        model,
        excludes=(
            'parent_id', 'children', 'type_', '_acl', 'id', 'parent',

        ),
    )


class StatisticSheetList(BaseView):
    """
    Listview of statistic sheets
    """
    title = u"Feuilles de statistiques"

    def __call__(self):
        statistics_js.need()
        sheets = StatisticSheet.query()
        sheets = sheets.order_by(desc(StatisticSheet.active)).all()

        submiturl = self.request.route_path(
            'statistics',
            _query=dict(action='add'),
        )

        return dict(sheets=sheets, title=self.title, submiturl=submiturl)


def statistic_sheet_add_edit_view(context, request):
    """
    View for adding editing statistics sheets
    """
    post_datas = request.POST or request.json_body
    if 'title' in post_datas:
        schema = SQLAlchemySchemaNode(StatisticSheet, includes=('title',))

        try:
            appstruct = schema.deserialize(request.POST)
        except colander.Invalid:
            logger.exception(u"Erreur à la création de la feuille de \
statistiques")
        else:
            if context.__name__ == 'statistic_sheet':
                sheet = schema.objectify(appstruct, context)
                sheet = request.dbsession.merge(sheet)
            else:
                sheet = schema.objectify(appstruct)
                request.dbsession.add(sheet)
            request.dbsession.flush()
            url = request.route_path('statistic', id=sheet.id)
            return dict(redirect=url)
        logger.debug(u"Invalid datas have been passed")
        raise HTTPClientError()
    logger.debug(u"Missing datas in the request")
    raise HTTPClientError()


def statistic_sheet_view(context, request):
    """
    Statistic sheet view
    """
    statistics_js.need()
    loadurl = request.route_path(
        'statistic',
        id=context.id,
        _query=dict(action='options'),
    )
    contexturl = request.current_route_path()

    request.actionmenu.add(
        widgets.ViewLink(
            u"Retour à la liste",
            "list_statistics",
            path="statistics",
        )
    )

    return dict(
        title=u"Feuille de statistiques",
        loadurl=loadurl,
        contexturl=contexturl,
    )


def convert_duple_to_dict(duple_list):
    return [{'value': option[0], 'label': option[1]} for option in duple_list]


def statistic_form_options(context, request):
    """
    Returns datas used to build the statistic form page
    """
    inspector = get_inspector()

    return dict(
        columns=inspector.get_json_columns(),
        sheet_edit_url=request.route_path(
            'statistic',
            id=context.id,
            _query=dict(action='edit')
        ),
        entry_root_url=request.route_path(
            'statistic_entries',
            id=context.id,
        ),
        optrel_options=load_optrel(inspector),
        static_opt_options=load_static_options(inspector),
        methods={
            'date': convert_duple_to_dict(DATE_OPTIONS),
            'number': convert_duple_to_dict(NUMERIC_OPTIONS),
            'string': convert_duple_to_dict(STRING_OPTIONS),
            'optrel': convert_duple_to_dict(OPTREL_OPTIONS),
            'static_opt': convert_duple_to_dict(OPTREL_OPTIONS),
            'bool': convert_duple_to_dict(BOOL_OPTIONS),
            'multidate': convert_duple_to_dict(MULTIDATE_OPTIONS),
        }
    )


def load_optrel(inspector):
    """
    Return the opt rel options
    """
    res = {}
    for key, column in inspector.columns.items():
        if column['type'] == 'optrel':
            rel_class = column['related_class']
            res[key] = [
                {
                    'label': getattr(option, 'label', u'Inconnu'),
                    'id': option.id,
                    'value': str(option.id),
                }
                for option in rel_class.query()
            ]
    return res


def load_static_options(inspector):
    """
    Return the options for static selectable elements
    """
    res = {}
    for key, column in inspector.columns.items():
        if column['type'] == 'static_opt' and 'options' in column:
            # It's a string column
            res[key] = [
                {
                    'label': option[1],
                    'value': option[0],
                }
                for option in column['options']
            ]
    return res


class StatisticDisableView(DisableView):
    """
    Sheet Disable view
    """
    enable_msg = u"La feuille de statistiques a été activée"
    disable_msg = u"La feuille de statistiques a été désactivée"
    redirect_route = "statistics"


class StatisticDuplicateView(DuplicateView):
    """
    Sheet Duplication view
    """
    message = u"Vous avez été redirigé vers la nouvelle feuille de statistique"
    route_name = "statistic"


class StatisticDeleteView(DeleteView):
    """
    Sheet Deletion view
    """
    delete_msg = u"La feuille de statistiques a bien été supprimée"
    redirect_route = "statistics"


class RestStatisticSheet(BaseRestView):
    """
    Json rest api for statistic sheet handling
    """

    @property
    def schema(self):
        return SQLAlchemySchemaNode(
            StatisticSheet,
            includes=('title',)
        )

    def get(self):
        return {
            'sheet': self.context,
            'entries': self.context.entries
        }


class RestStatisticEntry(BaseRestView):
    """
    Json rest api for statistic entries handling
    """
    @property
    def schema(self):
        return SQLAlchemySchemaNode(
            StatisticEntry,
            includes=('title', 'description',),
        )

    def collection_get(self):
        """
        Return the list of entries
        context is the parent sheet
        """
        return self.context.entries

    def post_format(self, entry, edit, attributes):
        if not edit:
            entry.sheet = self.context
        return entry


class RestStatisticCriterion(BaseRestView):
    """
    Api rest pour la gestion des critères statistiques
    """
    def get_schema(self, submitted):
        logger.debug("Looking for a schema : %s" % submitted)
        model_type = submitted['type']

        model = CRITERION_MODELS.get(model_type)

        schema = SQLAlchemySchemaNode(
            model,
            excludes=('type_', 'id'),
        )
        if model_type in ('or', 'and'):
            schema['criteria'] = colander.SchemaNode(
                colander.Sequence(),
                forms.get_sequence_child_item(
                    BaseStatisticCriterion,
                    child_attrs=('id', 'key')
                )[0],
                name='criteria',
                missing=colander.drop,
            )
        return schema

    def collection_get(self):
        """
        Return the list of top level criteria (not those combined in Or or And
        clauses
        context is the current entry
        """
        # Top level is handled on view side
        return self.context.criteria
        # return [criterion for criterion in self.context.criteria
        #         if not criterion.has_parent()]  # only top level

    def pre_format(self, values):
        """
        Since when serializing a multi select on the client side, we get a list
        OR a string, we need to enforce getting a string
        """
        if "criteria" in values:
            criteria_ids = values['criteria']
            if not hasattr(criteria_ids, '__iter__'):
                values['criteria'] = [criteria_ids]

        if 'searches' in values:
            searches = values.get('searches')
            if not hasattr(searches, '__iter__'):
                values['searches'] = [searches]
        return values

    def post_format(self, criterion, edit, attributes):
        """
        We hard-set the model_type
        """
        if not edit:
            criterion.entry = self.context

        return criterion


class CsvEntryView(UserDatasCsvView):
    """
    The view used to stream a the items matching a statistic entry
    """
    model = UserDatas

    def query(self):
        inspector = get_inspector()
        query_factory = EntryQueryFactory(UserDatas, self.context, inspector)
        query = query_factory.query()
        return query

    @property
    def filename(self):
        filename = "{0}.csv".format(ascii.force_ascii(self.context.title))
        return filename


class CsvSheetView(BaseView):
    """
    Return a csv sheet as a csv response
    """
    @property
    def filename(self):
        return u"{0}.csv".format(ascii.force_ascii(self.context.title))

    def __call__(self):
        query_factory = SheetQueryFactory(
            UserDatas,
            self.context,
            get_inspector()
        )

        writer = csv.CsvExporter()
        writer.set_headers(query_factory.headers)
        for row in query_factory.rows:
            writer.add_row(row)

        write_file_to_request(self.request, self.filename, writer.render())
        return self.request.response


def add_routes(config):
    """
    Add module's related routes
    """
    # Routes for statistic sheet view/add/edit/delete
    config.add_route(
        'statistics',
        '/statistics',
    )

    config.add_route(
        'statistic',
        '/statistics/{id:\d+}',
        traverse='/statistics/{id}',
    )

    config.add_route(
        'statistic_entries',
        '/statistics/{id}/entries',
        traverse='/statistics/{id}',
    )
    config.add_route(
        'statistic_entry',
        '/statistics/{id}/entries/{eid:\d+}',
        traverse='/statistic_entries/{eid}',
    )
    config.add_route(
        "statistic_criteria",
        "/statistics/{id}/entries/{eid:\d+}/criteria",
        traverse='/statistic_entries/{eid}',
    )
    config.add_route(
        "statistic_criterion",
        "/statistics/{id}/entries/{eid:\d+}/criteria/{cid:\d+}",
        traverse='/statistic_criteria/{cid}',
    )


def includeme(config):
    """
    Include views in the app's configuration
    """
    add_routes(config)

    config.add_view(
        StatisticSheetList,
        route_name='statistics',
        renderer="statistics/list.mako",
        permission='list_statistics',
    )

    config.add_view(
        statistic_sheet_add_edit_view,
        route_name="statistics",
        request_param="action=add",
        permission='add_statistic',
        renderer='json',
    )
    config.add_view(
        statistic_sheet_add_edit_view,
        route_name="statistic",
        request_param="action=edit",
        permission='edit_statistic',
        renderer='json',
    )

    config.add_view(
        statistic_form_options,
        route_name='statistic',
        renderer='json',
        xhr=True,
        request_method='GET',
        request_param="action=options",
        permission='edit_statistic',
    )

    config.add_view(
        statistic_sheet_view,
        route_name='statistic',
        renderer='statistics/edit.mako',
        permission="view_statistic",
    )

    config.add_view(
        StatisticDisableView,
        route_name="statistic",
        request_param="action=disable",
        permission='edit_statistic',
    )
    config.add_view(
        StatisticDeleteView,
        route_name="statistic",
        request_param="action=delete",
        permission='edit_statistic',
    )

    config.add_view(
        StatisticDuplicateView,
        route_name="statistic",
        request_param="action=duplicate",
        permission='edit_statistic',
    )

    for attr, perm in (('put', 'edit',), ('get', 'view',)):
        config.add_view(
            RestStatisticSheet,
            attr=attr,
            route_name='statistic',
            request_method=attr.upper(),
            permission='%s_statistic' % perm,
            renderer='json',
            xhr=True,
        )

    for attr, perm in (
        ('put', 'edit',), ('get', 'view',), ('delete', 'edit',)
    ):
        config.add_view(
            RestStatisticEntry,
            attr=attr,
            route_name='statistic_entry',
            request_method=attr.upper(),
            permission='%s_statistic' % perm,
            renderer='json',
            xhr=True,
        )
        config.add_view(
            RestStatisticCriterion,
            attr=attr,
            route_name='statistic_criterion',
            request_method=attr.upper(),
            permission='%s_statistic' % perm,
            renderer='json',
            xhr=True,
        )

    for attr, method, perm in (
        ('post', 'post', 'edit'),
        ('collection_get', 'get', 'view')
    ):
        config.add_view(
            RestStatisticEntry,
            attr=attr,
            route_name='statistic_entries',
            request_method=method.upper(),
            permission='%s_statistic' % perm,
            renderer='json',
            xhr=True,
        )
        config.add_view(
            RestStatisticCriterion,
            attr=attr,
            route_name='statistic_criteria',
            request_method=method.upper(),
            permission='%s_statistic' % perm,
            renderer='json',
            xhr=True,
        )

    # Csv export views
    config.add_view(
        CsvEntryView,
        route_name='statistic_entry',
        permission='view_statistic',
        request_param="format=csv",
    )

    config.add_view(
        CsvSheetView,
        route_name='statistic',
        permission='view_statistic',
        request_param="format=csv",
    )
