# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#
import pytest


@pytest.fixture
def customer2(dbsession, company):
    from autonomie.models.customer import Customer
    customer = Customer(
        name=u"customer2",
        code=u"CUST",
        lastname=u"Lastname",
        firstname=u"Firstname",
        address=u"1th street",
        zip_code=u"01234",
        city=u"City",
    )
    customer.company = company
    dbsession.add(customer)
    dbsession.flush()
    return customer

def getone():
    from autonomie.models.project import Project
    return Project.query().first()


def test_add(company, get_csrf_request_with_db, config, customer):
    from autonomie.views.project import ProjectAdd
    config.add_route('project', '/')
    req = get_csrf_request_with_db()
    req.context = company
    view = ProjectAdd(req)

    appstruct = {'name':u'Projéct&$', "code":"ABDC", "customers": [customer.id]}
    view.submit_success(appstruct)

    project = getone()

    assert project.name == u'Projéct&$'
    assert project.code == "ABDC"
    assert project.company_id == company.id
    assert len(project.customers) == 1

def test_edit(config, get_csrf_request_with_db, customer, project):
    from autonomie.views.project import ProjectEdit
    config.add_route('project', '/')
    req = get_csrf_request_with_db()
    req.context = project
    definition = u"Super project, should e ^dmeù*"
    appstruct = {
        'name':u'Projéct&$', "code":"ABDC", "customers": [customer.id],
        'definition': definition
    }
    view = ProjectEdit(req)
    view.submit_success(appstruct)

    project = getone()
    assert(project.definition ==  definition)

def test_customer_remove(config, get_csrf_request_with_db, project):
    assert len(project.customers) ==  1
    from autonomie.views.project import ProjectEdit
    config.add_route('project', '/')
    req = get_csrf_request_with_db()
    req.context = project
    appstruct = {
        'name': project.name,
        "code": project.code,
        "customers": []
    }
    view = ProjectEdit(req)
    view.submit_success(appstruct)

    project = getone()
    assert(len(project.customers) == 0)

def test_customer_add(config,
                      project, customer, customer2, get_csrf_request_with_db):
    from autonomie.views.project import ProjectEdit
    config.add_route('project', '/')
    req = get_csrf_request_with_db()
    req.context = project
    appstruct = {
        'name': project.name,
        "code": project.code,
        "customers": [customer.id, customer2.id]
    }
    view = ProjectEdit(req)
    view.submit_success(appstruct)
    project = getone()
    assert(len(project.customers) == 2)

def test_delete(project, get_csrf_request_with_db):
    from autonomie.views.project import project_delete
    req = get_csrf_request_with_db()
    req.referer = "test"
    project = getone()
    req.context = project
    project_delete(req)
    assert(getone() is None)

def test_archive(project, get_csrf_request_with_db):
    from autonomie.views.project import project_archive
    req = get_csrf_request_with_db()
    req.referer = "test"
    req.context = project
    project_archive(req)
    assert(getone().archived)

def test_addphase(config, dbsession, phase, project, get_csrf_request_with_db):
    from autonomie.views.project import PhaseAddFormView
    from autonomie.models.project import Phase
    config.add_route('project', '/')
    req = get_csrf_request_with_db()
    req.context = project
    view = PhaseAddFormView(req)
    view.submit_success({'name': u'Phasé'})
    dbsession.flush()
    phases = Phase.query().filter(Phase.project==project).all()
    assert(len(phases) == 2)

def test_editphase(config, dbsession, project, get_csrf_request_with_db):
    from autonomie.views.project import PhaseEditFormView
    from autonomie.models.project import Phase
    phase = Phase(name='test', project=project)
    dbsession.merge(phase)
    dbsession.flush()

    config.add_route('project', '/')
    req = get_csrf_request_with_db()
    req.context = phase
    view = PhaseEditFormView(req)
    view.submit_success({'name': u'Phasé'})
    dbsession.flush()
    phase = Phase.get(phase.id)
    assert(phase.name == u'Phasé')
