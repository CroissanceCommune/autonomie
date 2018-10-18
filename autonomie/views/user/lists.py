# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
User and user datas listing views
"""
import logging

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
from autonomie.models.user.group import Group

from autonomie.views import BaseListView


logger = logging.getLogger(__name__)


class BaseUserListView(BaseListView):
    """
    Base list for the User model
    Provide :

        The base User class query
        The filtering on the search field
        The filtering on the company activity_id

    add filters to specify more specific list views (e.g: trainers, users with
    account ...)
    """
    title = u"Tous les comptes"
    schema = None
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

    def filter_user_group(self, query, appstruct):
        group_id = appstruct.get('group_id');
        if group_id:
            query = query.filter(
                User.login.has(
                    Login.groups.any(
                        Group.id == group_id
                    )
                )
            )
        return query


class GeneralAccountList(BaseUserListView):
    """
    List the User models with Login attached to them

    Allows to filter on :

        * Active/unactive Login
        * Company name or User lastname/firstname
        * Company acivity

    Sort on:
        * User.lastname
        * User.email
    """
    title = u"Annuaire des utilisateurs"
    # The schema used to validate our search/filter form
    schema = get_list_schema()
    # The columns that allow sorting
    sort_columns = dict(
        name=User.lastname,
        email=User.email,
    )

    def filter_login_filter(self, query, appstruct):
        """
        Filter the list on accounts with login only
        """
        query = query.join(User.login)
        login_filter = appstruct.get('login_filter', 'active_login')
        logger.debug("Filtering login : %s" % login_filter)
        if login_filter == 'active_login':
            logger.debug("Adding a filter on Login.active")
            query = query.filter(Login.active == True)
        elif login_filter == "unactive_login":
            query = query.filter(Login.active == False)
        return query


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
        active = appstruct.get('active', 'Y')
        if active == 'Y':
            query = query.filter(Login.active == True)
        elif active == "N":
            query = query.filter(Login.active == False)
        return query

    def filter_user_group(self, query, appstruct):
        group_id = appstruct.get('group_id');
        if group_id:
            query = query.filter(
                User.login.any(
                    Login.groups.any(
                        Group.id == group_id
                    )
                )
            )
        return query


def includeme(config):
    """
    Pyramid module entry point

    :param obj config: The pyramid configuration object
    """
    config.add_view(
        GeneralAccountList,
        route_name='/users',
        renderer='/user/lists.mako',
        permission='visit'
    )
