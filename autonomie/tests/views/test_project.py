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
from autonomie.models.project import Project
from autonomie.models.company import Company


APPSTRUCT = {'name':u'Projéct&$', "code":"ABDC", "customers":["1"]}

@pytest.fixture
def project(config, get_csrf_request_with_db):
    from autonomie.views.project import ProjectAdd
    config.add_route('project', '/')
    req = get_csrf_request_with_db()
    company = Company.query().first()
    company.__name__ = 'company'
    req.context = company
    view = ProjectAdd(req)
    appstruct = APPSTRUCT.copy()
    view.submit_success(appstruct)
    return getone()


def getone():
    val = Project.query().filter(Project.name=="Projéct&$").first()
    if val is not None:
        val.__name__ = 'project'
    return val


@pytest.fixture
def customer(dbsession):
    from autonomie.models.customer import Customer
    datas = {'name':'Company', 'contactLastName':u'Lastname',
             'contactFirstName':u'FirstName',
             'address':'Address should be multiline',
             'zipCode': "21000",
             "city": "Dijon",
             'compte_cg':"Compte CG1515",
             'compte_tiers':"Compte Tiers", 'code': 'CODE'}
    c = Customer(**datas)
    dbsession.add(c)
    dbsession.flush()
    return c


def test_add(project):
    assert project.code == "ABDC"
    assert project.company_id == 1
    assert len(project.customers) == 1

def test_edit(project, get_csrf_request_with_db):
    from autonomie.views.project import ProjectEdit
    req = get_csrf_request_with_db()
    req.context = project
    appstruct = APPSTRUCT.copy()
    definition = u"Super project, should e ^dmeù*"
    appstruct['definition'] = definition
    view = ProjectEdit(req)
    view.submit_success(appstruct)
    project = getone()
    assert(project.definition ==  definition)

def test_customer_remove(project, get_csrf_request_with_db):
    from autonomie.views.project import ProjectEdit
    req = get_csrf_request_with_db()
    req.context = project
    appstruct = APPSTRUCT.copy()
    appstruct["customers"] = []
    view = ProjectEdit(req)
    view.submit_success(appstruct)
    project = getone()
    assert(len(project.customers) == 0)

def test_customer_add(project, customer, get_csrf_request_with_db):
    from autonomie.views.project import ProjectEdit
    req = get_csrf_request_with_db()
    req.context = project
    appstruct = APPSTRUCT.copy()
    appstruct['customers'] = ["1", customer.id]
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

def test_addphase(config, dbsession, project, get_csrf_request_with_db):
    from autonomie.views.project import PhaseAddFormView
    from autonomie.models.project import Phase
    config.add_route('project/{id}', '/')
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

    config.add_route('project/{id}', '/')
    req = get_csrf_request_with_db()
    req.context = phase
    view = PhaseEditFormView(req)
    view.submit_success({'name': u'Phasé'})
    dbsession.flush()
    phase = Phase.get(phase.id)
    assert(phase.name == u'Phasé')
