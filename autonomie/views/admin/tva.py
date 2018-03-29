# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Tva administration tools
"""
from pyramid.httpexceptions import HTTPFound
from autonomie.models.tva import Tva
from autonomie.views import (
    BaseView,
    DisableView,
    BaseAddView,
    BaseEditView,
)
from autonomie.utils.widgets import Link
from autonomie.views import render_api
from autonomie.views.admin.tools import AdminCrudListView
from autonomie.forms.admin import get_tva_edit_schema


class TvaListView(AdminCrudListView):
    """
    List of tva entries
    """
    title = u"Configuration comptable des produits et TVA collectés"
    columns = [u"Libellé", u"Valeur", u"Compte CG de TVA", u"Défaut ?"]
    back_route = "admin_vente"

    def stream_columns(self, tva):
        """
        Stream the table datas for the given item
        :param obj tva: The Tva object to stream
        :returns: List of labels
        """
        if tva.default:
            default = u"<i class='glyphicon glyphicon-ok-sign'></i> \
Tva par défaut"
        else:
            default = ""
        return (
            tva.name,
            render_api.format_amount(tva.value),
            tva.compte_cg or u"Aucun",
            default,
        )

    def stream_actions(self, tva):
        """
        Stream the actions available for the given tva object
        :param obj tva: Tva instance
        :returns: List of 5-uples (url, label, title, icon, disable)
        """
        yield Link(
            self.request.route_path(
                "/admin/vente/tvas/",
                id=tva.id
            ),
            u"Voir/Modifier",
            icon=u"pencil",
        )
        if tva.active:
            yield Link(
                self.request.route_path(
                    "/admin/vente/tvas/",
                    id=tva.id,
                    _query=dict(action='disable'),
                ),
                label=u"Désactiver",
                title=u"La TVA n'apparaitra plus dans l'interface",
                icon=u"remove",
            )
            if not tva.default:
                yield Link(
                    self.request.route_path(
                        "/admin/vente/tvas/",
                        id=tva.id,
                        _query=dict(action='set_default'),
                    ),
                    label=u"Définir comme Taux de Tva par défaut",
                    title=u"La TVA sera sélectionnée par défaut dans les "
                    u"formulaires",
                )
        else:
            yield Link(
                self.request.route_path(
                    "/admin/vente/tvas/",
                    id=tva.id,
                    _query=dict(action='disable'),
                ),
                u"Activer",
                title=u"La TVA apparaitra plus dans l'interface",
            )

    def load_items(self):
        return Tva.query(include_inactive=True).all()

    def more_template_vars(self, result):
        if result['items']:
            if Tva.get_default() is None:
                result['warn_msg'] = (
                    u"Aucun taux de TVA par défaut n'a été configuré. "
                    u"Des problèmes peuvent être rencontrés lors de "
                    u"l'édition de devis/factures."
                )
        return result

    def get_addurl(self):
        return self.request.route_path(
            '/admin/vente/tvas',
            _query=dict(action="new")
        )


class TvaDisableView(DisableView):
    disable_msg = u"Le taux de TVA a bien été désactivé"
    enable_msg = u"Le taux de TVA a bien été activé"
    redirect_route = "/admin/vente/tvas"


class TvaEditView(BaseEditView):
    """
    Edit view
    """
    add_template_vars = ('menus', 'help_msg')
    schema = get_tva_edit_schema()
    factory = Tva
    redirect_route = "/admin/vente/tvas"

    menus = [
        dict(
            label=u"Retour",
            route_name="/admin/vente/tvas",
            icon="fa fa-step-backward"
        )
    ]
    title = u"Modifier"

    def submit_success(self, appstruct):
        old_products = []
        for product in self.context.products:
            if product.id not in [p.get('id') for p in appstruct['products']]:
                product.active = False
                old_products.append(product)
        model = self.schema.objectify(appstruct, self.context)
        model.products.extend(old_products)
        self.dbsession.merge(model)
        self.dbsession.flush()

        if self.msg:
            self.request.session.flash(self.msg)

        if hasattr(self, 'redirect'):
            return self.redirect()
        elif self.redirect_route is not None:
            return HTTPFound(self.request.route_path(self.redirect_route))


class TvaAddView(BaseAddView):
    """
    Add view
    """
    add_template_vars = ('menus', 'help_msg')
    schema = get_tva_edit_schema()
    factory = Tva
    redirect_route = "/admin/vente/tvas"
    menus = [
        dict(
            label=u"Retour",
            route_name="/admin/vente/tvas",
            icon="fa fa-step-backward"
        )
    ]
    title = u"Ajouter"


class TvaSetDefaultView(BaseView):
    """
    Set the given tva as default
    """
    def __call__(self):
        for tva in Tva.query(include_inactive=True):
            tva.default = False
            self.request.dbsession.merge(tva)
        self.context.default = True
        self.request.dbsession.merge(tva)
        return HTTPFound(self.request.route_path('/admin/vente/tvas'))


def includeme(config):
    """
    Add routes and views
    """
    config.add_route('/admin/vente/tvas', '/admin/vente/tvas')
    config.add_route(
        '/admin/vente/tvas/',
        '/admin/vente/tvas/{id}',
        traverse="/tvas/{id}"
    )

    config.add_view(
        TvaListView,
        route_name='/admin/vente/tvas',
        permission='admin',
        renderer='admin/crud_list.mako',
    )
    config.add_view(
        TvaDisableView,
        route_name='/admin/vente/tvas/',
        permission='admin',
        request_param="action=disable",
        renderer='admin/crud_list.mako',
    )
    config.add_view(
        TvaAddView,
        route_name='/admin/vente/tvas',
        permission='admin',
        request_param="action=new",
        renderer='admin/crud_add_edit.mako',
    )
    config.add_view(
        TvaEditView,
        route_name='/admin/vente/tvas/',
        permission='admin',
        renderer='admin/crud_add_edit.mako',
    )
    config.add_view(
        TvaSetDefaultView,
        route_name='/admin/vente/tvas/',
        permission='admin',
        request_param="action=set_default",
    )
