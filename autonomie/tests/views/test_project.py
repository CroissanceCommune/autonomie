# -*- coding: utf-8 -*-
# * File Name : test_project.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-10-2012
# * Last Modified :
#
# * Project :
#
from mock import MagicMock
from autonomie.models.project import Project
from autonomie.views.project import (ProjectAdd, ProjectEdit,
        project_addphase, project_archive, project_delete)

from autonomie.tests.base import BaseFunctionnalTest

APPSTRUCT = {'name':u'Projéct&$', "code":"ABDC", "clients":[]}

class Base(BaseFunctionnalTest):
    def addOne(self, appstruct=APPSTRUCT):
        self.config.add_route('project', '/')
        req = self.get_csrf_request()
        req.context = MagicMock(id=1)
        view = ProjectAdd(req)
        view.submit_success(appstruct)

    def getOne(self):
        try:
            return Project.query().filter(Project.name=="Projéct&$").one()
        except:
            return None

class TestProjectAdd(Base):
    def test_success(self):
        self.addOne()
        project = self.getOne()
        self.assertEqual(project.code, "ABDC")
        self.assertEqual(project.company_id, 1)

    def test_client_not_exist(self):
        appstruct = {'name':u'Projéct&$', "code":"ABDC", "clients":["11111"]}
        self.addOne(appstruct)
        project = self.getOne()
        self.assertEqual(len(project.clients), 0)

    def test_client(self):
        from autonomie.models.client import Client
        print Client.get(1)
        appstruct = {'name':u'Projéct&$', "code":"ABDC", "clients":["1"]}
        self.addOne(appstruct)
        project = self.getOne()
        self.assertEqual(len(project.clients), 1)


class TestProjectEdit(Base):
    def test_edit(self):
        self.addOne()
        project = self.getOne()
        req = self.get_csrf_request()
        req.context = project
        appstruct = APPSTRUCT.copy()
        definition = u"Super project, should e ^dmeù*"
        appstruct['definition'] = definition
        view = ProjectEdit(req)
        view.submit_success(appstruct)
        project = self.getOne()
        self.assertEqual(project.definition, definition)

    def test_client_remove(self):
        appstruct = {'name':u'Projéct&$', "code":"ABDC", "clients":["1"]}
        self.addOne(appstruct)
        project = self.getOne()
        req = self.get_csrf_request()
        req.context = project
        appstruct["clients"] = []
        view = ProjectEdit(req)
        view.submit_success(appstruct)
        project = self.getOne()
        self.assertEqual(len(project.clients), 0)

    def test_client_add(self):
        self.addOne()
        project = self.getOne()
        req = self.get_csrf_request()
        req.context = project
        appstruct = APPSTRUCT.copy()
        appstruct['clients'] = ["1"]
        view = ProjectEdit(req)
        view.submit_success(appstruct)
        project = self.getOne()
        self.assertEqual(len(project.clients), 1)

class TestActions(Base):
    def test_delete(self):
        self.addOne()
        req = self.get_csrf_request()
        req.referer = "test"
        project = self.getOne()
        req.context = project
        project_delete(req)
        self.assertEqual(self.getOne(), None)

    def test_archive(self):
        self.addOne()
        req = self.get_csrf_request()
        req.referer = "test"
        project = self.getOne()
        req.context = project
        project_archive(req)
        self.assertEqual(self.getOne().archived, 1)

    def test_addphase(self):
        self.addOne()
        req = self.get_csrf_request()
        req.referer = "test"
        project = self.getOne()
        req.context = project
        req.params['phase'] = u'Phasé'
        project_addphase(req)
        self.assertEqual(len(self.getOne().phases), 2)


