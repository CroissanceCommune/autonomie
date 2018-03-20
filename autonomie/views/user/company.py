# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

from pyramid.httpexceptions import HTTPFound

from autonomie.models.company import Company

from autonomie.forms.user.company import get_company_association_schema
from autonomie.views import (
    BaseView,
    BaseFormView,
)


class UserCompaniesView(BaseView):
    """
    Collect datas for the company display view
    """
    title = u"Entreprises"

    @property
    def current_user(self):
        return self.context

    def __call__(self):
        companies = self.current_user.companies
        return dict(
            companies=companies,
            user=self.current_user,
        )


class CompanyAssociationView(BaseFormView):
    """
    Associate a user with a company
    """
    title = u"Associer un utlisateur à une entreprise"
    schema = get_company_association_schema()

    @property
    def current_user(self):
        return self.context

    def submit_success(self, appstruct):
        for name in appstruct.get('companies', []):
            company = Company.query().filter(Company.name == name).first()
            if company is not None and \
                    company not in self.current_user.companies:
                self.current_user.companies.append(company)
                self.request.dbsession.merge(self.current_user)

        url = self.request.route_path(
            "/users/{id}/companies",
            id=self.current_user.id,
        )
        return HTTPFound(url)


def add_routes(config):
    config.add_route(
        '/users/{id}/companies',
        '/users/{id}/companies',
        traverse='/users/{id}',
    )
    for action in ('associate',):
        config.add_route(
            '/users/{id}/companies/%s' % action,
            '/users/{id}/companies/%s' % action,
            traverse='/users/{id}',
        )


def add_views(config):
    config.add_view(
        UserCompaniesView,
        route_name="/users/{id}/companies",
        layout="user",
        permission="view.company",
        renderer="autonomie:templates/user/companies.mako",
    )
    config.add_view(
        CompanyAssociationView,
        route_name='/users/{id}/companies/associate',
        renderer="autonomie:templates/base/formpage.mako",
        permission="edit.company",
        layout="default",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
