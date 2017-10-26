# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_new_task_schema(project, customer, phase, company):
    from pyramid.testing import DummyRequest
    from autonomie.tests.tools import Dummy
    from autonomie.forms.tasks.base import get_new_task_schema
    schema = get_new_task_schema()
    req = DummyRequest(
        context=project,
        matched_route=Dummy(name='project_estimations'),
        current_company=company,
    )
    schema = schema.bind(request=req)

    result = schema.deserialize({
        'name': u'Facture',
        'customer_id': str(customer.id),
        'project_id': str(project.id),
        'phase_id': str(phase.id),
        'course': str(1)
    })

    assert result == {
        'name': u'Facture',
        'customer_id': customer.id,
        'project_id': project.id,
        'phase_id': phase.id,
        'course': 1,
    }


