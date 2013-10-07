"""
    Index view
"""
import logging

from pyramid.httpexceptions import HTTPFound


log = logging.getLogger(__name__)


def index(request):
    """
        Index page
    """
    user = request.user
    companies = user.companies
    if user.is_admin() or user.is_manager():
        return HTTPFound(request.route_path('manage'))
    elif len(companies) == 1:
        company = companies[0]
        return HTTPFound(request.route_path('company', id=company.id,
                                            _query=dict(action='index')))
    else:
        for company in companies:
            company.url = request.route_path("company", id=company.id,
                                            _query=dict(action='index'))
        return dict(
                    title=u"Bienvenue dans Autonomie",
                    companies=user.companies)


def includeme(config):
    """
        Adding the index view on module inclusion
    """
    config.add_route("index", "/")
    config.add_view(index, route_name='index', renderer='index.mako')