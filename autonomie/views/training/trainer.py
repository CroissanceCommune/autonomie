# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
import logging
from sqlalchemy.orm import load_only

from pyramid.httpexceptions import HTTPFound
from deform_extensions import AccordionFormWidget
from js.deform import auto_need

from autonomie.utils.strings import (
    format_account,
)
from autonomie.models import files
from autonomie.models.training.trainer import TrainerDatas
from autonomie.forms.training.trainer import (
    get_add_edit_trainerdatas_schema,
    FORM_GRID,
)
from autonomie.utils.menu import AttrMenuDropdown
from autonomie.views import (
    BaseView,
    BaseEditView,
    DeleteView,
    submit_btn,
    cancel_btn,
)

logger = logging.getLogger(__name__)

USER_ITEM_URL = "/users/{id}"

TRAINER_URL = '/trainerdatas'
TRAINER_ITEM_URL = os.path.join(TRAINER_URL, "{id}")
TRAINER_FILE_URL = os.path.join(TRAINER_ITEM_URL, "filelist")
USER_TRAINER_URL = os.path.join(USER_ITEM_URL, "trainerdatas")
USER_TRAINER_ADD_URL = os.path.join(USER_TRAINER_URL, "add")
USER_TRAINER_EDIT_URL = os.path.join(USER_TRAINER_URL, "edit")
USER_TRAINER_FILE_URL = os.path.join(USER_TRAINER_URL, "filelist")

TRAINER_MENU = AttrMenuDropdown(
    name='trainerdatas',
    label=u"Formation",
    default_route=USER_TRAINER_URL,
    icon=u"fa fa-graduation-cap",
    hidden_attribute="trainerdatas",
    perm="view.trainerdatas",
)
TRAINER_MENU.add_item(
    name="trainerdatas_view",
    label=u"Fiche formateur",
    route_name=USER_TRAINER_EDIT_URL,
    icon=u'fa fa-user-circle-o',
    perm="edit.trainerdatas",
)
TRAINER_MENU.add_item(
    name="trainerdatas_filelist",
    label=u"Fichier liés à la formation",
    route_name=USER_TRAINER_FILE_URL,
    icon=u'fa fa-briefcase',
    perm="view.file",
)


def trainerdatas_add_entry_view(context, request):
    """
    Trainer datas add view

    :param obj context: The pyramid context (User instance)
    :param obj request: The pyramid request
    """
    logger.debug(u"Adding Trainer datas for the user %s" % context.id)
    trainerdatas = TrainerDatas(user_id=context.id)
    request.dbsession.add(trainerdatas)
    request.dbsession.flush()
    return HTTPFound(
        request.route_path(
            USER_TRAINER_EDIT_URL,
            id=context.id,
        )
    )


class TrainerDatasEditView(BaseEditView):
    """
    Trainer datas edition view
    """
    schema = get_add_edit_trainerdatas_schema()
    validation_msg = u"La fiche formateur a bien été enregistrée"
    buttons = (submit_btn, cancel_btn,)
    add_template_vars = ('delete_url', 'current_trainerdatas')

    @property
    def delete_url(self):
        return self.request.route_path(
            TRAINER_ITEM_URL,
            id=self.current_trainerdatas.id,
            _query={'action': 'delete'},
        )

    @property
    def title(self):
        return u"Fiche formateur de {0}".format(
            format_account(self.current_trainerdatas.user)
        )

    @property
    def current_trainerdatas(self):
        return self.context

    def before(self, form):
        auto_need(form)
        form.widget = AccordionFormWidget(named_grids=FORM_GRID)
        form.set_appstruct(self.schema.dictify(self.current_trainerdatas))


class UserTrainerDatasEditView(TrainerDatasEditView):
    @property
    def current_trainerdatas(self):
        return self.context.trainerdatas


class TrainerDatasDeleteView(DeleteView):
    """
    TrainerDatas deletion view
    """
    delete_msg = u"La fiche formateur a bien été supprimée"

    def redirect(self):
        return HTTPFound(
            self.request.route_path('/users/{id}', id=self.context.user_id)
        )


class TrainerDatasFileList(BaseView):
    @property
    def current_trainerdatas(self):
        return self.context

    def __call__(self):
        query = files.File.query().options(load_only(
            "description",
            "name",
            "updated_at",
            "id",
        ))
        query = query.filter_by(parent_id=self.current_trainerdatas.id)

        return dict(
            title=u"Documents formateur",
            files=query,
            current_trainerdatas=self.current_trainerdatas,
        )


class UserTrainerDatasFileList(TrainerDatasFileList):
    @property
    def current_trainerdatas(self):
        return self.context.trainerdatas


def add_routes(config):
    config.add_route(
        USER_TRAINER_URL,
        USER_TRAINER_URL,
        traverse="/users/{id}",
    )
    config.add_route(
        USER_TRAINER_ADD_URL,
        USER_TRAINER_ADD_URL,
        traverse="/users/{id}",
    )
    config.add_route(
        USER_TRAINER_EDIT_URL,
        USER_TRAINER_EDIT_URL,
        traverse="/users/{id}",
    )
    config.add_route(
        USER_TRAINER_FILE_URL,
        USER_TRAINER_FILE_URL,
        traverse="/users/{id}",
    )
    config.add_route(TRAINER_URL, TRAINER_URL)
    config.add_route(
        TRAINER_ITEM_URL, TRAINER_ITEM_URL, traverse="/trainerdatas/{id}"
    )
    config.add_route(
        TRAINER_FILE_URL, TRAINER_FILE_URL, traverse="/trainerdatas/{id}"
    )


def add_views(config):
    config.add_view(
        trainerdatas_add_entry_view,
        route_name=USER_TRAINER_ADD_URL,
        permission="add.trainerdatas",
    )
    config.add_view(
        TrainerDatasEditView,
        route_name=TRAINER_ITEM_URL,
        permission="edit.trainerdatas",
        renderer="autonomie:templates/training/trainerdatas_edit.mako",
        layout='user',
    )
    config.add_view(
        UserTrainerDatasEditView,
        route_name=USER_TRAINER_EDIT_URL,
        permission="edit.trainerdatas",
        renderer="autonomie:templates/training/trainerdatas_edit.mako",
        layout='user',
    )
    config.add_view(
        UserTrainerDatasFileList,
        route_name=USER_TRAINER_FILE_URL,
        permission="filelist.trainerdatas",
        renderer="autonomie:templates/training/filelist.mako",
        layout="user",
    )
    config.add_view(
        TrainerDatasFileList,
        route_name=TRAINER_FILE_URL,
        permission="filelist.trainerdatas",
        renderer="autonomie:templates/training/filelist.mako",
        layout="user",
    )

    config.add_view(
        TrainerDatasDeleteView,
        route_name=TRAINER_ITEM_URL,
        permission="delete.trainerdatas",
        request_param="action=delete",
        layout='default',
    )


def register_menus():
    from autonomie.views.user.layout import UserMenu
    UserMenu.add(TRAINER_MENU)


def includeme(config):
    """
    Pyramid main entry point

    :param obj config: The current application config object
    """
    add_routes(config)
    add_views(config)

    register_menus()
