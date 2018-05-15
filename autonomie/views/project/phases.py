# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

from pyramid.httpexceptions import HTTPFound

from autonomie.models.project import (
    Phase,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.forms.project import (
    PhaseSchema,
)
from autonomie.views import BaseFormView
from autonomie.views.project.routes import (
    PROJECT_ITEM_ROUTE,
    PHASE_ITEM_ROUTE,
    PROJECT_ITEM_PHASE_ROUTE,
)


log = logger = logging.getLogger(__name__)


class PhaseAddFormView(BaseFormView):
    title = u"Ajouter un dossier au projet"
    schema = PhaseSchema()

    def submit_success(self, appstruct):
        model = Phase()
        model.project_id = self.context.id
        merge_session_with_post(model, appstruct)
        self.dbsession.add(model)
        self.dbsession.flush()
        redirect = self.request.route_path(
            PROJECT_ITEM_PHASE_ROUTE,
            id=model.project_id,
            _query={'phase': model.id}
        )
        return HTTPFound(redirect)


class PhaseEditFormView(BaseFormView):
    title = u"Modification du dossier"
    schema = PhaseSchema()

    def before(self, form):
        form.set_appstruct(self.context.appstruct())

    def submit_success(self, appstruct):
        merge_session_with_post(self.context, appstruct)
        self.dbsession.merge(self.context)
        redirect = self.request.route_path(
            PROJECT_ITEM_PHASE_ROUTE,
            id=self.context.project_id,
        )
        return HTTPFound(redirect)


def phase_delete_view(context, request):
    """
    Phase deletion view

    Allows to delete phases without documents
    :param obj context: The current phase
    :param obj request: The pyramid request object
    """
    redirect = request.route_path(
        PROJECT_ITEM_PHASE_ROUTE,
        id=context.project_id,
    )
    if len(context.tasks) == 0:
        msg = u"Le dossier {0} a été supprimé".format(context.name)
        request.dbsession.delete(context)
        request.session.flash(msg)
    else:
        msg = u"Impossible de supprimer le dossier {0}, il contient \
des documents".format(context.name)
        request.session.flash(msg, 'error')
    return HTTPFound(redirect)


def includeme(config):
    config.add_view(
        PhaseAddFormView,
        route_name=PROJECT_ITEM_ROUTE,
        request_param="action=addphase",
        renderer="base/formpage.mako",
        permission='edit_project',
        layout='default'
    )
    config.add_view(
        PhaseEditFormView,
        route_name=PHASE_ITEM_ROUTE,
        renderer="base/formpage.mako",
        permission='edit_phase',
    )
    config.add_view(
        phase_delete_view,
        route_name=PHASE_ITEM_ROUTE,
        renderer="base/formpage.mako",
        permission='edit_phase',
        request_param="action=delete",
    )
