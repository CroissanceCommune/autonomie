# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models.project.phase import Phase
from autonomie.views.project.routes import (
    PROJECT_ITEM_PHASE_ROUTE,
)
from autonomie.views.project.phase import (
    PhaseAddFormView,
    PhaseEditFormView,
    phase_delete_view,
)


def test_addphase(config, dbsession, phase, project, get_csrf_request_with_db):
    config.add_route(PROJECT_ITEM_PHASE_ROUTE, PROJECT_ITEM_PHASE_ROUTE)
    req = get_csrf_request_with_db()
    req.context = project
    view = PhaseAddFormView(req)
    view.submit_success({'name': u'Phasé'})
    dbsession.flush()
    phases = Phase.query().filter(Phase.project == project).all()
    assert(len(phases) == 2)


def test_editphase(config, dbsession, project, get_csrf_request_with_db):
    phase = Phase(name='test', project=project)
    dbsession.merge(phase)
    dbsession.flush()

    config.add_route(PROJECT_ITEM_PHASE_ROUTE, PROJECT_ITEM_PHASE_ROUTE)
    req = get_csrf_request_with_db()
    req.context = phase
    view = PhaseEditFormView(req)
    view.submit_success({'name': u'Phasé'})
    dbsession.flush()
    phase = Phase.get(phase.id)
    assert(phase.name == u'Phasé')


def test_delete_phase(
    config, dbsession, project, phase, get_csrf_request_with_db
):
    config.add_route(PROJECT_ITEM_PHASE_ROUTE, PROJECT_ITEM_PHASE_ROUTE)
    req = get_csrf_request_with_db()
    req.context = phase

    result = phase_delete_view(phase, req)
    assert result.location == PROJECT_ITEM_PHASE_ROUTE.format(id=project.id)
