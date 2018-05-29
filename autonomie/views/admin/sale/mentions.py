# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os

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
        u"Titre",
    ]
    factory = TaskMention

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
    """.format(self.request.route_path(BUSINESS_MENTION_URL))

    def stream_columns(self, item):
        yield item.label
        yield item.title

    def stream_actions(self, item):
        yield Link(
            self._get_item_url(item),
            u"Voir/Modifier",
            icon=u"pencil",
        )
        if item.active:
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

    def load_items(self):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = TaskMention.query()
        items = items.order_by(self.factory.active).order_by(self.factory.label)
        return items

    def more_template_vars(self, result):
        result['help_msg'] = self.help_msg
        return result


class TaskMentionDisableView(BaseAdminDisableView):
    """
    View for TaskMention disable/enable
    """
    route_name = TASK_MENTION_ITEM_URL


class TaskMentionDeleteView(BaseAdminDeleteView):
    """
    TaskMention deletion view
    """
    route_name = TASK_MENTION_ITEM_URL


class TaskMentionAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = TASK_MENTION_URL
    factory = TaskMention
    schema = get_admin_task_mention_schema()


class TaskMentionEditView(BaseAdminEditView):
    route_name = TASK_MENTION_ITEM_URL
    factory = TaskMention
    schema = get_admin_task_mention_schema()

    help_msg = TaskMentionListView.help_msg

    @property
    def title(self):
        return u"Modifier la mention '{0}'".format(self.context.label)


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
