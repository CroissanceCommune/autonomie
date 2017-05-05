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
from autonomie.views import render_api
from autonomie.forms.admin import get_tva_edit_schema
TEMPLATES_URL = 'autonomie:deform_templates/'


class TvaListView(BaseView):
    """
    List of tva entries
    """
    title = u"Configuration comptable des produits et TVA collectés"

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
        yield (
            self.request.route_path(
                "/admin/vente/tvas/",
                id=tva.id
            ),
            u"Voir/Modifier",
            u"Voir/Modifier",
            u"pencil",
        )
        if tva.active:
            yield (
                self.request.route_path(
                    "/admin/vente/tvas/",
                    id=tva.id,
                    _query=dict(action='disable'),
                ),
                u"Désactiver",
                u"La TVA n'apparaitra plus dans l'interface",
                u"remove",
            )
            if not tva.default:
                yield (
                    self.request.route_path(
                        "/admin/vente/tvas/",
                        id=tva.id,
                        _query=dict(action='set_default'),
                    ),
                    u"Définir comme Taux de Tva par défaut",
                    u"La TVA sera sélectionnée par défaut dans les formulaires",
                    u"",
                )
        else:
            yield (
                self.request.route_path(
                    "/admin/vente/tvas/",
                    id=tva.id,
                    _query=dict(action='disable'),
                ),
                u"Activer",
                u"La TVA apparaitra plus dans l'interface",
                u"",
            )

    def __call__(self):
        menus = [dict(label=u"Retour", path="admin_vente",
                      icon="fa fa-step-backward")]
        columns = [
            u"Libellé", u"Valeur", u"Compte CG de TVA", u"Défaut ?"
        ]

        items = Tva.query(include_inactive=True).all()

        warn_msg = None
        if items:
            if Tva.get_default() is None:
                warn_msg = (u"Aucun taux de TVA par défaut n'a été configuré."
                            u"Des problèmes peuvent être rencontré lors de "
                            u"l'édition de devis/factures")

        return dict(
            items=items,
            warn_msg=warn_msg,
            columns=columns,
            stream_columns=self.stream_columns,
            stream_actions=self.stream_actions,
            title=self.title,
            menus=menus,
            addurl=self.request.route_path(
                '/admin/vente/tvas',
                _query=dict(action="new")
            ),
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

    menus = [
        dict(
            label=u"Retour",
            path="/admin/vente/tvas",
            icon="fa fa-step-backward"
        )
    ]
    title = u"Modifier"


class TvaAddView(BaseAddView):
    """
    Add view
    """
    add_template_vars = ('menus', 'help_msg')
    schema = get_tva_edit_schema()
    factory = Tva
    menus = [
        dict(
            label=u"Retour",
            path="/admin/vente/tvas",
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
