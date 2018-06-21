# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
from autonomie.tests.tools import Dummy
from autonomie.models.services.sale_file_requirements import (
    SaleFileRequirementService,
    TaskFileRequirementService,
    BusinessFileRequirementService,
)


@pytest.fixture
def ftypes(mk_business_type, mk_file_type):
    ftypes = {}
    for t in ('ftype1', 'ftype2', 'ftype3', 'ftype4'):
        ftypes[t] = mk_file_type(t)
    return ftypes


@pytest.fixture
def btypes(mk_business_type):
    btypes = {}
    for b in ('default', 'training'):
        btypes[b] = mk_business_type(b)
    return btypes


@pytest.fixture
def mk_dummy_invoice(mk_business_type_file_types, ftypes, btypes):
    from autonomie.models.services.sale_file_requirements import (
        SaleFileRequirementService,
    )

    def func(req_type='mandatory', validation=False, business=None, project=None):
        mk_business_type_file_types(
            ftypes['ftype1'], btypes['default'], 'invoice', req_type, validation
        )
        node = Dummy(
            file_requirements=[],
            type_='invoice',
            business_type_id=btypes['default'].id,
            business=business,
            project=project,
        )
        SaleFileRequirementService.populate(node)
        return node
    return func


@pytest.fixture
def mk_dummy_business(mk_business_type_file_types, ftypes, btypes):
    def func(req_type="mandatory", validation=False, tasks=[], project=None):
        from autonomie.models.services.sale_file_requirements import (
            SaleFileRequirementService,
        )
        business_node = Dummy(
            type_='business',
            file_requirements=[],
            business_type_id=btypes['default'].id,
            tasks=tasks,
            project=project,
        )
        mk_business_type_file_types(
            ftypes['ftype1'], btypes['default'], 'business',
            req_type, validation
        )
        SaleFileRequirementService.populate(business_node)
        return business_node
    return func


@pytest.fixture
def dummy_project(ftypes):
    node = Dummy(
        files=[Dummy(file_type_id=ftypes['ftype1'].id, id=1)]
    )
    return node


def test_base_populate(mk_dummy_invoice, ftypes):
    node = mk_dummy_invoice()
    assert len(node.file_requirements) == 1
    assert node.file_requirements[0].requirement_type == 'mandatory'
    assert node.file_requirements[0].file_type_id == ftypes['ftype1'].id
    assert node.file_requirements[0].status == 'danger'
    assert node.file_requirements[0].validation_status == 'valid'


def test_populate_recommended(mk_dummy_invoice):
    node = mk_dummy_invoice('recommended')
    assert node.file_requirements[0].requirement_type == 'recommended'
    assert node.file_requirements[0].status == 'warning'
    assert node.file_requirements[0].validation_status == 'valid'


def test_populate_validation(mk_dummy_invoice):
    node = mk_dummy_invoice(validation=True)
    assert node.file_requirements[0].status == 'danger'
    assert node.file_requirements[0].validation_status == 'none'


def test_populate_void(mk_business_type_file_types, ftypes, btypes):
    mk_business_type_file_types(
        ftypes['ftype1'], btypes['default'], 'invoice', 'recommended'
    )
    node = Dummy(
        file_requirements=[],
        type_='estimation',
        business_type_id=btypes['default'].id,
    )
    SaleFileRequirementService.populate(node)
    assert len(node.file_requirements) == 0


def test_check_task_files_no_ok(mk_dummy_invoice, mk_dummy_business):
    invoice = mk_dummy_invoice()
    business = mk_dummy_business(tasks=[invoice])
    BusinessFileRequirementService.check_task_files(business)
    assert business.file_requirements[0].status == 'danger'


def test_check_task_files_ok(mk_dummy_invoice, mk_dummy_business):
    invoice = mk_dummy_invoice()
    invoice.file_requirements[0].status = 'success'
    invoice.file_requirements[0].file_id = 1

    business = mk_dummy_business(tasks=[invoice])
    BusinessFileRequirementService.check_task_files(business)
    assert business.file_requirements[0].status == 'success'
    assert business.file_requirements[0].file_id == 1


def test_check_task_files_validation_wait(mk_dummy_invoice, mk_dummy_business):
    invoice = mk_dummy_invoice()
    invoice.file_requirements[0].status = 'warning'
    invoice.file_requirements[0].file_id = 1
    invoice.file_requirements[0].validation_status = 'wait'

    business = mk_dummy_business(validation=True, tasks=[invoice])
    BusinessFileRequirementService.check_task_files(business)
    assert business.file_requirements[0].status == 'warning'
    assert business.file_requirements[0].validation_status == 'wait'
    assert business.file_requirements[0].file_id == 1


def test_check_business_files_scope_ok(mk_dummy_business, mk_dummy_invoice):
    business = mk_dummy_business()
    invoice = mk_dummy_invoice(business=business)
    TaskFileRequirementService.check_business_files(invoice)

    assert invoice.file_requirements[0].status == "danger"


def test_check_business_files_scope_nook(mk_dummy_business, mk_dummy_invoice):
    business = mk_dummy_business()
    business.file_requirements[0].status = "success"
    business.file_requirements[0].file_id = 1

    invoice = mk_dummy_invoice("business_mandatory", business=business)
    TaskFileRequirementService.check_business_files(invoice)

    assert invoice.file_requirements[0].status == "success"


def test_check_project_files_scope_ok(mk_dummy_invoice, dummy_project):
    invoice = mk_dummy_invoice(project=dummy_project)
    TaskFileRequirementService.check_project_files(invoice)
    print(invoice.file_requirements[0].requirement_type)

    assert invoice.file_requirements[0].status == "danger"


def test_check_project_files_scope_nook(mk_dummy_invoice, dummy_project):
    invoice = mk_dummy_invoice('project_mandatory', project=dummy_project)
    TaskFileRequirementService.check_project_files(invoice)

    assert invoice.file_requirements[0].status == "success"
