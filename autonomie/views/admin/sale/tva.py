# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Tva administration tools
"""
import os
from pyramid.httpexceptions import HTTPFound
from autonomie.models.tva import Tva
from autonomie.views import (
    BaseView,
)
from autonomie.utils.widgets import Link
from autonomie.forms.admin import get_tva_edit_schema
from autonomie.views import render_api
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminEditView,
    AdminTreeMixin,
    BaseAdminAddView,
    BaseAdminDisableView,
)
from autonomie.views.admin.sale import (
    SALE_URL,
    SaleIndexView,
)

TVA_URL = os.path.join(SALE_URL, 'tva')
TVA_ITEM_URL = os.path.join(TVA_URL, '{id}')


class TvaListView(AdminCrudListView):
    """
    List of tva entries
    """
    title = u"Configuration comptable des produits et TVA collectés"
    description = u"Configurer : Taux de TVA, codes produits et codes \
analytiques associés"
    route_name = TVA_URL
    columns = [u"Libellé", u"Valeur", u"Compte CG de TVA", u"Défaut ?"]

    item_route_name = TVA_ITEM_URL

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
            self._get_item_url(tva),
            u"Voir/Modifier",
            icon=u"pencil",
        )
        if tva.active:
            yield Link(
                self._get_item_url(tva, action='disable'),
                label=u"Désactiver",
                title=u"La TVA n'apparaitra plus dans l'interface",
                icon=u"remove",
            )
            if not tva.default:
                yield Link(
                    self._get_item_url(tva, action='set_default'),
                    label=u"Définir comme Taux de Tva par défaut",
                    title=u"La TVA sera sélectionnée par défaut dans les "
                    u"formulaires",
                )
        else:
            yield Link(
                self._get_item_url(tva, action='disable'),
                u"Activer",
                title=u"La TVA apparaitra plus dans l'interface",
                icon="fa fa-check",
            )

    def load_items(self):
        return Tva.query(include_inactive=True).all()

    def more_template_vars(self, result):
        result['nodata_msg'] = u"Aucun taux de TVA n'a été configuré"
        if result['items']:
            if Tva.get_default() is None:
                result['warn_msg'] = (
                    u"Aucun taux de TVA par défaut n'a été configuré. "
                    u"Des problèmes peuvent être rencontrés lors de "
                    u"l'édition de devis/factures."
                )
        return result


class TvaDisableView(BaseAdminDisableView):
    route_name = TVA_ITEM_URL
    disable_msg = u"Le taux de TVA a bien été désactivé"
    enable_msg = u"Le taux de TVA a bien été activé"


class TvaEditView(BaseAdminEditView):
    """
    Edit view
    """
    route_name = TVA_ITEM_URL

    schema = get_tva_edit_schema()
    factory = Tva
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

        return self.redirect()


class TvaAddView(BaseAdminAddView):
    """
    Add view
    """
    route_name = TVA_URL
    schema = get_tva_edit_schema()
    factory = Tva
    title = u"Ajouter"


class TvaSetDefaultView(BaseView, AdminTreeMixin):
    """
    Set the given tva as default
    """
    route_name = TVA_ITEM_URL

    def __call__(self):
        for tva in Tva.query(include_inactive=True):
            tva.default = False
            self.request.dbsession.merge(tva)
        self.context.default = True
        self.request.dbsession.merge(tva)
        return HTTPFound(TVA_URL)


def includeme(config):
    """
    Add routes and views
    """
    config.add_route(TVA_URL, TVA_URL)
    config.add_route(TVA_ITEM_URL, TVA_ITEM_URL, traverse="/tvas/{id}")

    config.add_admin_view(
        TvaListView,
        parent=SaleIndexView,
        renderer='admin/crud_list.mako',
    )
    config.add_admin_view(
        TvaDisableView,
        parent=TvaListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        TvaAddView,
        parent=TvaListView,
        request_param="action=add",
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        TvaEditView,
        parent=TvaListView,
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        TvaSetDefaultView,
        parent=TvaListView,
        request_param="action=set_default",
    )
