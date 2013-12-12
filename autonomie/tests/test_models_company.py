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
import datetime

from mock import MagicMock
from autonomie.models.company import Company
from autonomie.models.customer import Customer
from autonomie.models.project import Phase
from autonomie.models.project import Project
from autonomie.models.task import Estimation
from .base import BaseTestCase

TEST = dict(name=u"Test",
            logo=u"logo.png",
            header=u"header.png",
            id=1)


class TestCompanyModel(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.company = Company(name=u"Test", id=1)
        self.company.logo = dict(filename=u"logo.png")
        self.company.header = dict(filename=u"header.png")

    def test_get_path(self):
        self.assertEqual(self.company.get_path(), "company/1")
        self.assertEqual(self.company.get_logo_filepath(), "company/1/logo/logo.png")
        self.assertEqual(self.company.get_header_filepath(), "company/1/header/header.png")

    def test_get_company_id(self):
        self.assertEqual(self.company.get_company_id(), 1)

    def test_get_tasks(self):
        # specific setup
        for project_name, project_code in (
            ('project_%d' % num, 'PC%2d' % num)
            for num in xrange(12)):

            project = Project(name=project_name, code=project_code)
            
            for customer, time in (
                (Customer(), time) 
                for time in xrange(3)): 

                customer.name = 'cust_%d_%s' % (time, project_name)
                project.customers.append(customer)
                project.company = self

            for phase in (Phase('phase_%d' % time) for time in xrange(3)):
                project.append(phase)

        # setup the part that is to be tested
            for estimation in (Estimation() for time in xrange(4)):
                estimation.project = project
                # FIXME: something that is to be tested
                # tasks will be ordered according to dates.
                estimation_date = datetime.date(2013, 01, 01)
                estimation.taskDate = estimation_date
            self.company.projects.append(project)

        # FIXME: actually test

    def test_get_recent_tasks(self):
        pass
