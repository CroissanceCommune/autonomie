# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

from pyramid.httpexceptions import HTTPFound

from autonomie.models.company import Company

from autonomie.utils.widgets import Link
from autonomie.utils.strings import format_account
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

    def _stream_actions(self, item):
        """
        Stream actions available for the given item

        :param obj item: The company instance
        """
        yield Link(
            self.request.route_path(
                "company",
                id=item.id,
            ),
            u"Voir",
            title=u"Voir l'enseigne",
            icon="search",
        )
        if self.request.has_permission('edit.company', item):
            yield Link(
                self.request.route_path(
                    "company",
                    id=item.id,
                ),
                u"Modifier",
                title=u"Modifier les informations relatives à l'enseigne",
                icon="pencil",
            )
        if self.request.has_permission("admin.company"):
            if len(item.employees) > 1:
                yield Link(
                    self.request.route_path(
                        "company",
                        id=item.id,
                        _query={'action': 'remove', id: self.current_user.id}
                    ),
                    u"Retirer",
                    title=u"Retirer l'entrepreneur de cette enseigne",
                    icon="link",
                    confirm=u"{} n'aura plus accès aux données de cette "
                    u"l'enseigne {}. Êtes-vous sûr de vouloir continuer "
                    u"?".format(
                        format_account(self.current_user),
                        item.name
                    )
                )

            if item.active:
                yield Link(
                    self.request.route_path(
                        "company",
                        id=item.id,
                        _query={'action': 'disable'}
                    ),
                    u"Désactiver",
                    title=u"Désactiver cette enseigne",
                    icon="book",
                    confirm=u"L'enseigne {} ne sera plus accessible et "
                    u"n'apparaîtra plus dans les listes (factures, notes de "
                    u"dépenses ...) Êtes-vous sûr de vouloir continuer "
                    u"?".format(item.name)
                )
            else:
                yield Link(
                    self.request.route_path(
                        "company",
                        id=item.id,
                        _query={'action': 'enable'}
                    ),
                    u"Activer",
                    title=u"Ré-activer cette enseigne",
                    icon="book",
                )

    def __call__(self):
        companies = self.current_user.companies
        return dict(
            companies=companies,
            user=self.current_user,
            stream_actions=self._stream_actions
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
        permission="list.company",
        renderer="autonomie:templates/user/companies.mako",
    )
    config.add_view(
        CompanyAssociationView,
        route_name='/users/{id}/companies/associate',
        renderer="autonomie:templates/base/formpage.mako",
        permission="admin.company",
        layout="default",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
