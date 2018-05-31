# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

import pytest


@pytest.fixture
def company2(dbsession, user):
    from autonomie.models.company import Company
    company = Company(
        name=u"Company 2",
        email=u"company2@c.fr",
    )
    company.employees = [user]
    dbsession.add(company)
    dbsession.flush()
    user.companies = [company]
    user = dbsession.merge(user)
    dbsession.flush()
    return company


@pytest.fixture
def customer2(dbsession, company2):
    from autonomie.models.customer import Customer
    customer = Customer(
        name=u"customer 2",
        code=u"CUS2",
        lastname=u"Lastname2",
        firstname=u"Firstname2",
        address=u"1th street",
        zip_code=u"01234",
        city=u"City",
    )
    customer.company = company2
    dbsession.add(customer)
    dbsession.flush()
    return customer


@pytest.fixture
def project2(dbsession, company2, customer2, project_type):
    from autonomie.models.project import Project
    project = Project(name=u"Project 2", project_type=project_type)
    project.company = company2
    project.customers = [customer2]
    dbsession.add(project)
    dbsession.flush()
    return project


@pytest.fixture
def phase2(dbsession, project2):
    from autonomie.models.project import Phase
    phase = Phase(name=u"Phase")
    phase.project = project2
    phase.project_id = project2.id
    project2.phases.append(phase)
    dbsession.add(phase)
    dbsession.flush()
    return phase


def test_new_task_schema(
    project, customer, phase, company, phase2, project2, default_business_type):
    import colander
    from pyramid.testing import DummyRequest
    from autonomie.tests.tools import Dummy
    from autonomie.forms.tasks.base import get_new_task_schema
    from autonomie.views.project.routes import PROJECT_ITEM_ESTIMATION_ROUTE
    schema = get_new_task_schema()
    req = DummyRequest(
        context=project,
        matched_route=Dummy(name=PROJECT_ITEM_ESTIMATION_ROUTE),
        current_company=company,
    )
    schema = schema.bind(request=req)

    result = schema.deserialize({
        'name': u'Facture',
        'customer_id': str(customer.id),
        'project_id': str(project.id),
        'phase_id': str(phase.id),
        'business_type_id': str(default_business_type.id),
    })

    assert result == {
        'name': u'Facture',
        'customer_id': customer.id,
        'project_id': project.id,
        'phase_id': phase.id,
        "business_type_id": default_business_type.id
    }
    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'name': u'Facture',
            'customer_id': str(customer.id),
            'project_id': str(project.id),
            'phase_id': str(phase2.id),
            "business_type_id": str(default_business_type.id)
        })

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'name': u'Facture',
            'customer_id': str(customer.id),
            'project_id': str(project2.id),
            'phase_id': str(phase2.id),
            "business_type_id": str(default_business_type.id)
        })

    with pytest.raises(colander.Invalid):
        schema.deserialize({
            'name': u'Facture',
            'customer_id': str(customer.id),
            'project_id': str(project2.id),
            'phase_id': str(phase2.id),
        })
