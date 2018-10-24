# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy.orm import (
    load_only,
)
from pyramid.httpexceptions import HTTPFound

from autonomie.models import files

from autonomie.views import (
    BaseView,
)
from autonomie.views.files import FileUploadView
from autonomie.views.userdatas.userdatas import USERDATAS_MENU
from autonomie.views.userdatas.routes import (
    USERDATAS_FILELIST_URL,
    USERDATAS_ITEM_URL,
    USER_USERDATAS_FILELIST_URL,
    USER_USERDATAS_MYDOCUMENTS_URL,
)
USERDATAS_MENU.add_item(
    name="userdatas_filelist",
    label=u'Portefeuille de documents',
    route_name=USER_USERDATAS_FILELIST_URL,
    icon=u'fa fa-briefcase',
    perm='filelist.userdatas',
)


class UserDatasFileAddView(FileUploadView):
    def redirect(self, come_from):
        return HTTPFound(
            self.request.route_path(
                USER_USERDATAS_FILELIST_URL,
                id=self.context.user.id,
            )
        )


class UserDatasFileList(BaseView):
    help_message = u"""
    Cette liste présente l'ensemble des documents déposés dans Autonomie ainsi
    que l'ensemble des documents générés depuis l'onglet Génération de
    documents.<br />Ces documents sont visibles par l'entrepreneur.
    """

    @property
    def current_userdatas(self):
        return self.context

    def __call__(self):
        query = files.File.query().options(load_only(
            "description",
            "name",
            "updated_at",
            "id",
        ))
        query = query.filter_by(parent_id=self.current_userdatas.id)

        return dict(
            title=u"Portefeuille de documents",
            files=query,
            add_url=self.request.route_path(
                '/userdatas/{id}',
                id=self.current_userdatas.id,
                _query=dict(action='attach_file')
            ),
            help_message=self.help_message,
        )


class UserUserDatasFileList(UserDatasFileList):
    @property
    def current_userdatas(self):
        return self.context.userdatas


def mydocuments_view(context, request):
    """
    View callable collecting datas for showing the social docs associated to the
    current user's account
    """
    if context.userdatas is not None:
        query = files.File.query()
        documents = query.filter(
            files.File.parent_id == context.userdatas.id
        ).all()
    else:
        documents = []
    return dict(
        title=u"Mes documents",
        documents=documents,
    )


def includeme(config):
    config.add_view(
        UserDatasFileAddView,
        route_name=USERDATAS_ITEM_URL,
        permission="addfile.userdatas",
        request_param='action=attach_file',
        layout='default',
        renderer="autonomie:templates/base/formpage.mako",
    )
    config.add_view(
        UserDatasFileList,
        route_name=USERDATAS_FILELIST_URL,
        permission="filelist.userdatas",
        renderer="/userdatas/filelist.mako",
        layout="user"
    )
    config.add_view(
        UserUserDatasFileList,
        route_name=USER_USERDATAS_FILELIST_URL,
        permission="filelist.userdatas",
        renderer="/userdatas/filelist.mako",
        layout="user"
    )
    config.add_view(
        mydocuments_view,
        route_name=USER_USERDATAS_MYDOCUMENTS_URL,
        permission="filelist.userdatas",
        renderer="/userdatas/mydocuments.mako",
        layout='user',
    )
