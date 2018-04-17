# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import colander

from sqlalchemy import (
    or_,
    distinct,
)
from pyramid.httpexceptions import HTTPFound

from autonomie_celery.tasks.export import export_to_file
from autonomie_celery.models import FileGenerationJob

from autonomie.models.user.userdatas import (
    UserDatas,
    CompanyDatas,
)
from autonomie.forms.user.userdatas import get_list_schema
from autonomie.utils.renderer import set_close_popup_response
from autonomie.views import BaseListView
from autonomie.views.userdatas.routes import (
    USERDATAS_URL,
    USERDATAS_XLS_URL,
    USERDATAS_CSV_URL,
    USERDATAS_ODS_URL,
    USER_USERDATAS_EDIT_URL,
    USERDATAS_ITEM_URL,
)


logger = logging.getLogger(__name__)


class UserDatasListClass(object):
    """
    User datas list view
    """
    title = u"Liste des informations sociales"
    schema = get_list_schema()
    sort_columns = dict(
        lastname=UserDatas.coordonnees_lastname,
    )
    default_sort = 'lastname'

    def query(self):
        return UserDatas.query()

    def filter_situation_situation(self, query, appstruct):
        """
        Filter the general situation of the project
        """
        logger.debug("APPSTRUCT : %s" % appstruct)
        situation = appstruct.get('situation_situation')
        if situation not in (None, '', colander.null):
            query = query.filter(
                UserDatas.situation_situation_id == situation
            )
        return query

    def filter_search(self, query, appstruct):
        """
        Filter the current query for firstname, lastname or activity
        """
        search = appstruct.get('search')

        if search not in (None, '', colander.null):
            filter_ = "%" + search + "%"
            query = query.filter(
                or_(
                    UserDatas.coordonnees_firstname.like(filter_),
                    UserDatas.coordonnees_lastname.like(filter_),
                    UserDatas.activity_companydatas.any(
                        CompanyDatas.name.like(filter_)),
                    UserDatas.activity_companydatas.any(
                        CompanyDatas.title.like(filter_)),
                )
            )
        return query

    def filter_situation_follower_id(self, query, appstruct):
        """
        Filter the current query through followers
        """
        follower_id = appstruct.get('situation_follower_id')

        if follower_id not in (None, -1, colander.null):
            query = query.filter(
                UserDatas.situation_follower_id == follower_id
            )
        return query


class UserDatasListView(UserDatasListClass, BaseListView):
    """
    The userdatas listing view
    """
    add_template_vars = (
        'stream_actions',
    )

    def stream_actions(self, item):
        """
        Stream actions available for the given item
        """
        yield (
            self.request.route_path(
                USER_USERDATAS_EDIT_URL,
                id=item.user_id
            ),
            u"Voir",
            u"Voir / modifier les données de gestion sociales",
            u"pencil",
            {}
        )

        yield (
            self.request.route_path(
                USERDATAS_ITEM_URL,
                id=item.id,
                _query={'action': 'delete'}
            ),
            u"Supprimer",
            u"Supprimer ces données de gestion sociale",
            u"trash",
            {
                'onclick': u"return confirm('En supprimant cette fiche de "
                u"gestion sociale, vous supprimerez "
                u"également es données associées (documents sociaux, "
                u"historique de situation ...). Continuez ?');"
            }
        )


class UserDatasXlsView(UserDatasListClass, BaseListView):
    """Userdatas excel view"""
    model = UserDatas
    file_format = "xls"
    filename = "gestion_sociale_"

    def query(self):
        return self.request.dbsession.query(distinct(UserDatas.id))

    def _build_return_value(self, schema, appstruct, query):
        """
        Return the streamed file object
        """
        all_ids = [elem[0] for elem in query]

        if not all_ids:
            msg = u"Il n'y a aucun élément à exporter"
            set_close_popup_response(self.request, msg)
            return self.request.response

        job = FileGenerationJob()
        job.set_owner(self.request.user.login.login)
        self.request.dbsession.add(job)
        self.request.dbsession.flush()
        celery_job = export_to_file.delay(
            job.id,
            'userdatas',
            all_ids,
            self.filename,
            self.file_format
        )

        logger.info(
            u"The Celery Task {0} has been delayed, its result "
            "sould be retrieved from the FileGenerationJob {1}".format(
                celery_job.id, job.id
            )
        )

        return HTTPFound(
            self.request.route_path('job', id=job.id, _query={'popup': 1})
        )


class UserDatasOdsView(UserDatasXlsView):
    file_format = 'ods'


class UserDatasCsvView(UserDatasXlsView):
    file_format = 'csv'


def add_routes(config):
    """
    Add module related routes
    """
    for route in (
        USERDATAS_URL,
        USERDATAS_XLS_URL,
        USERDATAS_CSV_URL,
        USERDATAS_ODS_URL,
    ):
        config.add_route(route, route)


def add_views(config):
    """
    Add module related views
    """
    config.add_view(
        UserDatasListView,
        route_name=USERDATAS_URL,
        renderer="/userdatas/list.mako",
        permission="admin_userdatas",
    )

    config.add_view(
        UserDatasXlsView,
        route_name=USERDATAS_XLS_URL,
        permission="admin_userdatas",
    )

    config.add_view(
        UserDatasOdsView,
        route_name=USERDATAS_ODS_URL,
        permission="admin_userdatas",
    )

    config.add_view(
        UserDatasCsvView,
        route_name=USERDATAS_CSV_URL,
        permission="admin_userdatas",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
