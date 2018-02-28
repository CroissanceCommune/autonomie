# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
User and user datas listing views
"""
import logging
import colander

from sqlalchemy import (
    or_,
    distinct,
)
from autonomie_base.models.base import DBSESSION

from autonomie.models.company import (
    Company,
    CompanyActivity,
)
from autonomie.models.user.user import User
from autonomie.models.user.login import Login
from autonomie.forms.user.user import get_list_schema

from autonomie.views import BaseListView


logger = logging.getLogger(__name__)


class GeneralUserList(BaseListView):
    """
        List the users
        Allows to search for companies or user name
        Sorting is allowed on names and emails
    """
    title = u"Annuaire des utilisateurs"
    # The schema used to validate our search/filter form
    schema = get_list_schema()
    # The columns that allow sorting
    sort_columns = dict(
        name=User.lastname,
        email=User.email,
    )

    def query(self):
        """
            Return the main query for our list view
        """
        logger.debug("Queryiing")
        query = DBSESSION().query(distinct(User.id), User)
        query = query.join(User.login)
        return query.outerjoin(User.companies)

    def filter_name_search(self, query, appstruct):
        """
            filter the query with the provided search argument
        """
        logger.debug("Filtering name")
        search = appstruct['search']
        if search:
            query = query.filter(
                or_(
                    User.lastname.like("%" + search + "%"),
                    User.firstname.like("%" + search + "%"),
                    User.companies.any(Company.name.like("%" + search + "%")),
                    User.companies.any(Company.goal.like("%" + search + "%"))
                )
            )

        return query

    def filter_activity_id(self, query, appstruct):
        """
        filter the query with company activities
        """
        logger.debug("Filtering by activity id")
        logger.debug(appstruct)
        activity_id = appstruct.get('activity_id')
        if activity_id:
            query = query.filter(
                User.companies.any(
                    Company.activities.any(
                        CompanyActivity.id == activity_id
                    )
                )
            )
            logger.debug(query)
        return query

    def filter_active(self, query, appstruct):
        active = appstruct.get('active')
        if active == 'Y':
            query = query.filter(Login.active == True)
        return query


def add_routes(config):
    """
    Add module related routes
    """
    config.add_route(
        "/users",
        "/users",
    )


def add_views(config):
    """
    Add module related views
    """
    config.add_view(
        GeneralUserList,
        route_name='/users',
        renderer='/user/lists.mako',
        permission='visit'
    )


def includeme(config):
    """
    Pyramid module entry point

    :param obj config: The pyramid configuration object
    """
    add_routes(config)
    add_views(config)
