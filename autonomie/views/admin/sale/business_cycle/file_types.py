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
from autonomie.models.project.file_types import BusinessTypeFileType
from autonomie.models.project.types import BusinessType
from autonomie.models.files import FileType

from autonomie.forms.admin.sale.business_cycle.file_types import (
    BusinessTypeFileTypeEntries,
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

BUSINESS_FILETYPE_URL = os.path.join(BUSINESS_URL, "business_type_file_type")


class BusinessTypeFileTypeView(BaseView, AdminTreeMixin):
    route_name = BUSINESS_FILETYPE_URL
    title = u"Fichiers obligatoires/facultatifs"
    description = u"Les fichiers qui doivent être déposés pour valider une \
affaire ou des documents étapes (devis/factures ...)"

    @property
    def help_message(self):
        from autonomie.views.admin.main.file_types import FILE_TYPE_ROUTE
        return u"""
    Configurer les obligations documentaires pour les différents types de
    documents.<br />
    Pour chaque <b>type d'affaire</b>, pour chaque <b>type de document</b> un
    type de fichier peut être  :
        <ul>
        <li><b>Globalement requis</b> :  Au moins un fichier de ce type doit
        être fourni dans l'affaire pour pouvoir valider le document
        </li>
        <li><b>Requis</b> : Pour chaque document (devis/facture), un fichier de
        ce type est requis pour la validation
        </li>
        <li>
        <b>Recommandé</b> : Un avertissement non bloquant sera indiqué si
        aucun fichier de ce type n'a été fourni.
        </li>
        <li>
        <b>Facultatif</b> : Ce type de fichier sera proposé à l'utilisateur lors
        du dépôt de fichier
        </li>
        </ul>
    NB : Les Types de fichiers sont configurables dans <a class='link'
    href="{0}">Configuration -> Configuratrion générale -> Type de fichiers
    déposables dans Autonomie</a>
    """.format(self.request.route_path(FILE_TYPE_ROUTE))

    def _collect_items(self):
        res = {}
        for item in BusinessTypeFileType.query():
            res.setdefault(
                item.file_type_id, {}
            ).setdefault(
                item.business_type_id, {}
            )[item.doctype] = {
                'requirement_type': item.requirement_type,
                'validation': item.validation
            }
        return res

    def __call__(self):
        return dict(
            business_types=BusinessType.query().all(),
            file_types=FileType.query().all(),
            items=self._collect_items(),
            breadcrumb=self.breadcrumb,
            back_link=self.back_link,
            help_message=self.help_message,
        )


class BusinessTypeFileTypeSetView(BaseView, AdminTreeMixin):
    schema = BusinessTypeFileTypeEntries

    def _find_item(self, appstruct, create=False):
        logger.debug(appstruct)
        file_type_id = appstruct['file_type_id']
        btype_id = appstruct['business_type_id']
        doctype = appstruct['doctype']
        res = BusinessTypeFileType.get((file_type_id, btype_id, doctype))
        if res is None and create:
            res = BusinessTypeFileType(
                file_type_id=file_type_id,
                business_type_id=btype_id,
                doctype=doctype
            )
        return res

    def __call__(self):
        schema = self.schema().bind(request=self.request)
        if 'submit' in self.request.params:
            controls = self.request.params.items()
            values = peppercorn.parse(controls)
            logger.debug(values)
            try:
                appstruct = schema.deserialize(values)
            except colander.Invalid:
                logger.exception(u"Error while validating association datas")
                self.request.session.flash(
                    u"Une erreur est survenue, veuillez "
                    u"contacter votre administrateur",
                    "error",
                )
            else:
                for datas in appstruct['items']:
                    requirement_type = datas.get('requirement_type')
                    if requirement_type is not None:
                        # Facultatif ou obligatoire : on retrouve ou on crée
                        obj = self._find_item(datas, create=True)
                        obj.requirement_type = requirement_type
                        validation = datas.get('validation')
                        obj.validation = validation == 'on'
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
    config.add_route(BUSINESS_FILETYPE_URL, BUSINESS_FILETYPE_URL)

    config.add_admin_view(
        BusinessTypeFileTypeView,
        request_method='GET',
        parent=BusinessCycleIndexView,
        renderer="autonomie:templates/admin/sale/"
        "business_type_file_type.mako"
    )
    config.add_view(
        BusinessTypeFileTypeSetView,
        route_name=BUSINESS_FILETYPE_URL,
        request_method='POST',
    )
