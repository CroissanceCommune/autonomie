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
def file_instance(dbsession, ftypes):
    from autonomie.models.files import File
    node = File(name="file01", file_type_id=ftypes['ftype1'].id, size=13,
                mimetype="text", )
    node.data = "test content"
    dbsession.add(node)
    dbsession.flush()
    return node


@pytest.fixture
def mk_invoice(
    dbsession, user, company, project,
    mk_business_type_file_types, ftypes, btypes,
):
    from autonomie.models.services.sale_file_requirements import (
        SaleFileRequirementService,
    )
    from autonomie.models.task import Invoice

    def func(req_type='mandatory', validation=False, add_req=True, **kwargs):
        if add_req:
            mk_business_type_file_types(
                ftypes['ftype1'],
                btypes['default'],
                'invoice',
                req_type,
                validation
            )
        if 'project' not in kwargs:
            kwargs['project'] = project
        node = Invoice(
            user=user,
            company=company,
            business_type_id=btypes['default'].id,
            **kwargs
        )
        dbsession.add(node)
        dbsession.flush()
        SaleFileRequirementService.populate(node)
        return node
    return func


@pytest.fixture
def mk_business(dbsession, mk_business_type_file_types, ftypes, btypes):
    from autonomie.models.services.sale_file_requirements import (
        SaleFileRequirementService,
    )
    from autonomie.models.project.business import Business

    def func(req_type="mandatory", validation=False, tasks=[], project=None):
        business_node = Business(
            file_requirements=[],
            business_type_id=btypes['default'].id,
            tasks=tasks,
            project=project,
        )
        mk_business_type_file_types(
            ftypes['ftype1'], btypes['default'], 'business',
            req_type, validation
        )
        dbsession.add(business_node)
        dbsession.flush()
        SaleFileRequirementService.populate(business_node)
        return business_node
    return func


@pytest.fixture
def project_with_file(project, file_instance):
    project.files = [file_instance]
    return project


def test_base_populate(mk_invoice, ftypes):
    node = mk_invoice()
    assert len(node.file_requirements) == 1
    assert node.file_requirements[0].requirement_type == 'mandatory'
    assert node.file_requirements[0].file_type_id == ftypes['ftype1'].id
    assert node.file_requirements[0].status == 'danger'
    assert node.file_requirements[0].validation_status == 'valid'


def test_populate_recommended(mk_invoice):
    node = mk_invoice('recommended')
    assert node.file_requirements[0].requirement_type == 'recommended'
    assert node.file_requirements[0].status == 'warning'
    assert node.file_requirements[0].validation_status == 'valid'


def test_populate_validation(mk_invoice):
    node = mk_invoice(validation=True)
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


def test_check_task_files_no_ok(mk_invoice, mk_business):
    invoice = mk_invoice()
    business = mk_business(tasks=[invoice])
    BusinessFileRequirementService.check_task_files(business)
    assert business.file_requirements[0].status == 'danger'


def test_check_task_files_ok(mk_invoice, mk_business, file_instance):
    invoice = mk_invoice()
    invoice.file_requirements[0].status = 'success'
    invoice.file_requirements[0].file_id = file_instance.id

    business = mk_business(tasks=[invoice])
    BusinessFileRequirementService.check_task_files(business)
    assert business.file_requirements[0].status == 'success'
    assert business.file_requirements[0].file_id == file_instance.id


def test_check_task_files_validation_wait(
    mk_invoice, mk_business, file_instance
):
    invoice = mk_invoice()
    invoice.file_requirements[0].status = 'warning'
    invoice.file_requirements[0].file_id = file_instance.id
    invoice.file_requirements[0].validation_status = 'wait'

    business = mk_business(validation=True, tasks=[invoice])
    BusinessFileRequirementService.check_task_files(business)
    assert business.file_requirements[0].status == 'warning'
    assert business.file_requirements[0].validation_status == 'wait'
    assert business.file_requirements[0].file_id == file_instance.id


def test_check_business_files_scope_ok(
    mk_business, mk_invoice, file_instance
):
    business = mk_business()
    invoice = mk_invoice(business_id=business.id)
    TaskFileRequirementService.check_business_files(invoice)

    assert invoice.file_requirements[0].status == "danger"


def test_check_business_files_scope_nook(
    mk_business, mk_invoice, file_instance
):
    business = mk_business()
    business.file_requirements[0].status = "success"
    business.file_requirements[0].file_id = file_instance.id

    invoice = mk_invoice("business_mandatory", business_id=business.id)
    TaskFileRequirementService.check_business_files(invoice)

    assert invoice.file_requirements[0].status == "success"


def test_check_project_files_scope_ok(mk_invoice, project_with_file):
    invoice = mk_invoice(project=project_with_file)
    TaskFileRequirementService.check_project_files(invoice)

    assert invoice.file_requirements[0].status == "danger"


def test_check_project_files_scope_nook(mk_invoice, project_with_file):
    invoice = mk_invoice('project_mandatory', project=project_with_file)
    TaskFileRequirementService.check_project_files(invoice)

    assert invoice.file_requirements[0].status == "success"


def test_check_project_business_files_scope_ok(
    mk_invoice, mk_business, project, file_instance
):
    other_business = mk_business("project_mandatory", project=project)
    other_business.file_requirements[0].status = 'success'
    other_business.file_requirements[0].file_id = file_instance.id

    invoice = mk_invoice("project_mandatory", project=project)
    TaskFileRequirementService.check_project_files(invoice)

    assert invoice.file_requirements[0].status == "success"


def test_check_project_business_files_scope_nook(
    mk_invoice, mk_business, project, file_instance
):
    other_business = mk_business("project_mandatory", project=project)
    other_business.file_requirements[0].status = 'success'
    other_business.file_requirements[0].file_id = file_instance.id

    invoice = mk_invoice("business_mandatory", project=project)
    TaskFileRequirementService.check_project_files(invoice)

    assert invoice.file_requirements[0].status == "danger"


def test_check_project_task_files_scope_ok(mk_invoice, project, file_instance):
    other_invoice = mk_invoice("project_mandatory", project=project)
    other_invoice.file_requirements[0].status = 'success'
    other_invoice.file_requirements[0].file_id = file_instance.id

    invoice = mk_invoice("project_mandatory", add_req=False, project=project)
    TaskFileRequirementService.check_project_files(invoice)

    assert invoice.file_requirements[0].status == "success"


def test_check_project_task_files_scope_nook(
    mk_invoice, project, file_instance
):
    other_invoice = mk_invoice("business_mandatory", project=project)
    other_invoice.file_requirements[0].status = 'success'
    other_invoice.file_requirements[0].file_id = file_instance.id

    invoice = mk_invoice("business_mandatory", add_req=False, project=project)
    TaskFileRequirementService.check_project_files(invoice)

    assert invoice.file_requirements[0].status == "danger"


def test_get_mandatory_indicators_mandatory(
    mk_invoice, mk_business, ftypes
):
    invoice = mk_invoice("mandatory")

    result = TaskFileRequirementService.get_mandatory_indicators(
        invoice.id, ftypes['ftype1'].id
    )
    assert len(result) == 1


def test_get_mandatory_indicators_recommended(
    mk_invoice, mk_business, ftypes
):
    invoice = mk_invoice("recommended")

    result = TaskFileRequirementService.get_mandatory_indicators(
        invoice.id, ftypes['ftype1'].id
    )
    assert len(result) == 1


def test_get_business_mandatory_indicators_task(
    mk_invoice, mk_business, ftypes
):
    invoice1 = mk_invoice("business_mandatory")
    business = mk_business("business_mandatory", tasks=[invoice1])

    result = TaskFileRequirementService.get_business_mandatory_indicators(
        business.id, ftypes['ftype1'].id
    )
    assert len(result) == 2


def test_get_business_mandatory_indicators_notask(
    mk_invoice, mk_business, ftypes
):
    invoice1 = mk_invoice("mandatory")
    business = mk_business("business_mandatory", tasks=[invoice1])

    result = TaskFileRequirementService.get_business_mandatory_indicators(
        business.id, ftypes['ftype1'].id
    )
    assert len(result) == 1


def test_get_project_mandatory_indicators_task(
    mk_invoice, mk_business, ftypes, project
):
    mk_invoice("project_mandatory", project=project)
    result = TaskFileRequirementService.get_project_mandatory_indicators(
        project.id, ftypes['ftype1'].id
    )
    assert len(result) == 1


def test_get_project_mandatory_indicators_business(
    mk_invoice, mk_business, ftypes, project
):
    mk_business("project_mandatory", project=project)
    result = TaskFileRequirementService.get_project_mandatory_indicators(
        project.id, ftypes['ftype1'].id
    )
    assert len(result) == 1


def test_get_file_related_indicators(
    dbsession, mk_invoice, mk_business, file_instance
):
    invoice = mk_invoice("mandatory")
    invoice.file_requirements[0].file_id = file_instance.id
    dbsession.merge(invoice.file_requirements[0])
    business = mk_business()
    business.file_requirements[0].file_id = file_instance.id
    dbsession.merge(business.file_requirements[0])

    res = SaleFileRequirementService.get_file_related_indicators(
        file_instance.id
    )
    dbsession.delete(file_instance)
    assert len(res) == 2
