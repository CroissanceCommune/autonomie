# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_customer_company_address(customer):
    assert customer.full_address == \
        u"""customer\n1th street\n01234 City"""
    customer.country = u"England"
    assert customer.full_address == \
        u"""customer\n1th street\n01234 City\nEngland"""


def test_customer_individual_address(individual_customer):
    assert individual_customer.full_address == \
        u"""M. et Mme Lastname Firstname\n1th street\n01234 City"""


def test_label_company(customer):
    assert customer.label == customer.name


def test_label_individual(individual_customer):
    assert individual_customer.label == u"""M. et Mme Lastname Firstname"""


def test_check_project_id(customer, project):
    from autonomie.models.customer import Customer
    assert Customer.check_project_id(customer.id, project.id)
    assert not Customer.check_project_id(customer.id, project.id + 1)
