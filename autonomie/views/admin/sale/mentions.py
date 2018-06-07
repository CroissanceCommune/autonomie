# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os

from sqlalchemy import asc, desc
from sqlalchemy.orm import load_only
from pyramid.httpexceptions import HTTPFound

from autonomie.models.task.mentions import (
    TaskMention,
)
from autonomie.utils.widgets import Link
from autonomie.forms.admin.sale.mentions import (
    get_admin_task_mention_schema,
)
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminDisableView,
    BaseAdminDeleteView,
    BaseAdminEditView,
    BaseAdminAddView,
)
from autonomie.views.admin.sale import (
    SALE_URL,
    SaleIndexView,
)

TASK_MENTION_URL = os.path.join(SALE_URL, "task_mentions")
TASK_MENTION_ITEM_URL = os.path.join(TASK_MENTION_URL, "{id}")


class TaskMentionListView(AdminCrudListView):
    title = u"Mentions des devis factures"
    description = u"Configurer les mentions à utiliser dans les devis et \
factures"

    route_name = TASK_MENTION_URL
    item_route_name = TASK_MENTION_ITEM_URL
    columns = [
        u"Libellé",
    ]
    factory = TaskMention

    def __init__(self, *args, **kwargs):
        AdminCrudListView.__init__(self, *args, **kwargs)
        self.max_order = TaskMention.get_next_order() - 1

    @property
    def help_msg(self):
        from autonomie.views.admin.sale.business_cycle.mentions import (
            BUSINESS_MENTION_URL
        )
        return u"""
    Configurez les mentions à utiliser dans les devis et factures.<br />
    Elles pourront ensuite être intégrées de manière obligatoire ou facultative
    dans les documents.<br />
    Pour cela, vous devez indiquer pour quel type de document elles
    doivent être utilisées en vous rendant dans <br /> <a class='link'
    href='{0}'>Configuration générale -> Module Ventes -> Cycle d'affaires ->
    Configuration des mentions obligatoires/facultatives</a>
    <br />
    <br />
    Des variables sont disponibles pour compléter les mentions :
        <ul>
        <li>
        <code>{{name}}</code> : Nom de l'activité
        </li>
        <li>
        <code>{{RIB}}</code> : RIB spécifique de l'activité
        </li>
        <li>
        <code>{{IBAN}}</code>: IBAN spécifique de l'activité
        </li>
        <li>
        <code>{{code_compta}}</code> : Code analytique de l'activité
        </li>
        </ul>
    """.format(self.request.route_path(BUSINESS_MENTION_URL))

    def stream_columns(self, item):
        yield item.label

    def stream_actions(self, item):
        yield Link(
            self._get_item_url(item),
            u"Voir/Modifier",
            icon=u"pencil",
        )
        move_url = self._get_item_url(item, action="move")
        if item.active:
            if item.order > 0:
                yield Link(
                    move_url + "&direction=up",
                    u"Remonter",
                    title=u"Remonter dans l'ordre des mentions",
                    icon=u"arrow-circle-o-up"
                )
            if item.order < self.max_order:
                yield Link(
                    move_url + "&direction=down",
                    u"Redescendre",
                    title=u"Redescendre dans l'ordre des mentions",
                    icon=u"arrow-circle-o-down"
                )

            yield Link(
                self._get_item_url(item, action='disable'),
                u"Désactiver",
                title=u"Cette mention ne sera plus insérée dans les documents",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(item, action='disable'),
                u"Activer",
                title=u"Cette mention sera insérée dans les documents",
                icon=u"check-square-o",
            )

        if not item.is_used:
            yield Link(
                self._get_item_url(item, action='delete'),
                u"Supprimer",
                icon=u"remove",
            )

    def load_items(self):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.request.dbsession.query(TaskMention).options(
            load_only('label',)
        )
        items = items.order_by(desc(self.factory.active))
        items = items.order_by(asc(self.factory.order))
        return items

    def more_template_vars(self, result):
        result['help_msg'] = self.help_msg
        return result


class TaskMentionAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = TASK_MENTION_URL
    factory = TaskMention
    schema = get_admin_task_mention_schema()

    def before(self, form):
        """
        Launched before the form is used

        :param obj form: The form object
        """
        pre_filled = {'order': self.factory.get_next_order()}
        form.set_appstruct(pre_filled)


class TaskMentionEditView(BaseAdminEditView):
    route_name = TASK_MENTION_ITEM_URL
    factory = TaskMention
    schema = get_admin_task_mention_schema()

    help_msg = TaskMentionListView.help_msg

    @property
    def title(self):
        return u"Modifier la mention '{0}'".format(self.context.label)


class TaskMentionDisableView(BaseAdminDisableView):
    """
    View for TaskMention disable/enable
    """
    route_name = TASK_MENTION_ITEM_URL

    def on_enable(self):
        """
        on enable we set order to the last one
        """
        order = TaskMention.get_next_order()
        self.context.order = order
        self.request.dbsession.merge(self.context)


class TaskMentionDeleteView(BaseAdminDeleteView):
    """
    TaskMention deletion view
    """
    route_name = TASK_MENTION_ITEM_URL


def move_view(context, request):
    """
    Reorder the current context moving it up in the category's hierarchy

    :param obj context: The given IncomeStatementMeasureType instance
    """
    action = request.params['direction']
    if action == 'up':
        context.move_up()
    else:
        context.move_down()
    return HTTPFound(request.route_path(TASK_MENTION_URL))


def includeme(config):
    config.add_route(
        TASK_MENTION_URL,
        TASK_MENTION_URL
    )
    config.add_route(
        TASK_MENTION_ITEM_URL,
        TASK_MENTION_ITEM_URL,
        traverse="/task_mentions/{id}"
    )
    config.add_admin_view(
        TaskMentionListView,
        parent=SaleIndexView,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        TaskMentionAddView,
        parent=TaskMentionListView,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
    )
    config.add_admin_view(
        TaskMentionEditView,
        parent=TaskMentionListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        TaskMentionDisableView,
        parent=TaskMentionListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        TaskMentionDeleteView,
        parent=TaskMentionListView,
        request_param="action=delete",
    )
    config.add_admin_view(
        move_view,
        route_name=TASK_MENTION_ITEM_URL,
        request_param='action=move',
    )
