# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
import colander
import peppercorn
import logging

from pyramid.httpexceptions import HTTPFound
from autonomie.models.project.mentions import BusinessTypeTaskMention
from autonomie.models.project.types import BusinessType
from autonomie.models.task.mentions import TaskMention

from autonomie.forms.admin.sale.business_cycle.mentions import (
    BusinessTypeMentionEntries,
)
from autonomie.views import BaseView
from autonomie.views.admin.tools import (
    AdminTreeMixin,
)
from autonomie.views.admin.sale.business_cycle import (
    BUSINESS_URL,
    BusinessCycleIndexView,
)
logger = logging.getLogger(__name__)

BUSINESS_MENTION_URL = os.path.join(BUSINESS_URL, "business_type_task_mention")


class BusinessTypeTaskMentionView(BaseView, AdminTreeMixin):
    route_name = BUSINESS_MENTION_URL
    title = u"Configuration des mentions obligatoires/facultatives"

    @property
    def help_message(self):
        from autonomie.views.admin.sale.mentions import TASK_MENTION_URL
        return u"""
    Configurer l'utilisation des mentions dans les différents documents.<br />
    Pour chaque <b>type d'affaire</b>, pour chaque <b>type de document</b> une
    mention peut être  :
        <ul>
        <li>
        <b>Facultative</b> : elle sera proposée à l'entrepreneur lors de
        l'édition de ses documents
        </li>
        <li>
        <b>Obligatoire</b> : elle sera
        automatiquement intégré dans les sorties PDF
        </li>
        </ul>
    NB : Les mentions sont configurables dans <a class='link'
    href="{0}">Configuration -> Module Ventes -> Mentions des devis et
    factures</a>
    """.format(self.request.route_path(TASK_MENTION_URL))

    def _collect_items(self):
        res = {}
        for item in BusinessTypeTaskMention.query():
            res.setdefault(
                item.task_mention_id, {}
            ).setdefault(
                item.business_type_id, {}
            )[item.doctype] = item.mandatory
        return res

    def __call__(self):
        return dict(
            business_types=BusinessType.query().all(),
            mentions=TaskMention.query().all(),
            items=self._collect_items(),
            breadcrumb=self.breadcrumb,
            back_link=self.back_link,
            help_message=self.help_message,
        )


class BusinessTypeTaskMentionSetView(BaseView, AdminTreeMixin):
    schema = BusinessTypeMentionEntries

    def _find_item(self, appstruct, create=False):
        logger.debug(appstruct)
        mention_id = appstruct['task_mention_id']
        btype_id = appstruct['business_type_id']
        doctype = appstruct['doctype']
        res = BusinessTypeTaskMention.get((mention_id, btype_id, doctype))
        if res is None and create:
            res = BusinessTypeTaskMention(
                task_mention_id=mention_id,
                business_type_id=btype_id,
                doctype=doctype
            )
        return res

    def __call__(self):
        schema = BusinessTypeMentionEntries().bind(request=self.request)
        if 'submit' in self.request.params:
            controls = self.request.params.items()
            values = peppercorn.parse(controls)
            logger.debug(values)
            try:
                appstruct = schema.deserialize(values)
            except colander.Invalid:
                logger.exception(u"Error while validating association datas")
                self.request.session.flash(u"Une erreur est survenue, veuillez "
                                           u"contacter votre administrateur")
            else:
                for datas in appstruct['items']:
                    mandatory = datas.get('mandatory')
                    if mandatory is not None:
                        # Facultatif ou obligatoire : on retrouve ou on crée
                        obj = self._find_item(datas, create=True)
                        obj.mandatory = mandatory == 'true'
                        self.request.dbsession.merge(obj)
                    else:
                        # Non utilisé : on supprime l'éventuel existant
                        obj = self._find_item(datas)
                        if obj is not None:
                            self.request.dbsession.delete(obj)
                self.request.session.flash(
                    u"Vos modifications ont été enregistrées"
                )

        return HTTPFound(self.request.current_route_path())


def includeme(config):
    config.add_route(BUSINESS_MENTION_URL, BUSINESS_MENTION_URL)

    config.add_admin_view(
        BusinessTypeTaskMentionView,
        request_method='GET',
        parent=BusinessCycleIndexView,
        renderer="autonomie:templates/admin/sale/"
        "business_type_task_mention.mako"
    )
    config.add_view(
        BusinessTypeTaskMentionSetView,
        route_name=BUSINESS_MENTION_URL,
        request_method='POST',
    )
