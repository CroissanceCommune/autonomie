# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


def test_is_deletable_void_project(project):
    assert not project.is_deletable()
    project.archived = True
    assert project.is_deletable()


def test_is_deletable_project_with_task(project, estimation):
    project.archived = True
    assert not project.is_deletable()


def test_get_next_estimation_index(project, estimation):
    assert project.get_next_estimation_index() == 2


def test_get_next_invoice_index(project, invoice):
    assert project.get_next_invoice_index() == 2


def test_get_next_cancelinvoice_index(project, cancelinvoice):
    assert project.get_next_cancelinvoice_index() == 2


def test_check_phase_id(project, phase):
    from autonomie.models.project import Project
    assert Project.check_phase_id(project.id, phase.id)


def test_customer_projects(project, customer):
    from autonomie.models.project import Project

    assert Project.get_customer_projects(customer.id) == [project]
