# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


@pytest.fixture
def tva(dbsession):
    from autonomie.models.tva import Tva
    tva = Tva(value=2000, name='20%')
    dbsession.add(tva)
    dbsession.flush()
    return tva


@pytest.fixture
def product(tva, dbsession):
    from autonomie.models.tva import Product
    product = Product(name='product', compte_cg='122', tva_id=tva.id)
    dbsession.add(product)
    dbsession.flush()
    return product


@pytest.fixture
def product_without_tva(dbsession):
    from autonomie.models.tva import Product
    product = Product(name='product', compte_cg='122')
    dbsession.add(product)
    dbsession.flush()
    return product


@pytest.fixture
def unity(dbsession):
    from autonomie.models.task.unity import WorkUnit
    print([w.label for w in WorkUnit.query()])
    unity = WorkUnit(label=u"Mètre")
    dbsession.add(unity)
    dbsession.flush()
    return unity


@pytest.fixture
def mention(dbsession):
    from autonomie.models.task.mentions import TaskMention
    mention = TaskMention(
        title=u"TaskMention tet",
        full_text=u"blabla",
        label=u"bla",
    )
    dbsession.add(mention)
    dbsession.flush()
    return mention


@pytest.fixture
def mode(dbsession):
    from autonomie.models.task.invoice import PaymentMode
    mode = PaymentMode(label=u"Chèque")
    dbsession.add(mode)
    dbsession.flush()
    return mode


@pytest.fixture
def bank(dbsession):
    from autonomie.models.task.invoice import BankAccount
    bank = BankAccount(label=u"banque", code_journal='bq', compte_cg='123')
    dbsession.add(bank)
    dbsession.flush()
    return bank


@pytest.fixture
def user(dbsession):
    from autonomie.models.user import User
    user = User(
        login=u"login",
        lastname=u"Lastname",
        firstname=u"Firstname",
        email="login@c.fr",
    )
    user.set_password('password')
    dbsession.add(user)
    dbsession.flush()
    return user


@pytest.fixture
def company(dbsession, user):
    from autonomie.models.company import Company
    company = Company(
        name=u"Company",
        email=u"company@c.fr",
    )
    company.employees = [user]
    dbsession.add(company)
    dbsession.flush()
    return company


@pytest.fixture
def customer(dbsession, company):
    from autonomie.models.customer import Customer
    customer = Customer(
        name=u"customer",
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


@pytest.fixture
def project(dbsession, company, customer):
    from autonomie.models.project import Project
    project = Project(name=u"Project")
    project.company = company
    project.customer = [customer]
    dbsession.add(project)
    dbsession.flush()
    return project


@pytest.fixture
def phase(dbsession, project):
    from autonomie.models.project import Phase
    phase = Phase(name=u"Phase")
    phase.project = project
    dbsession.add(phase)
    dbsession.flush()
    return phase


@pytest.fixture
def task_line_group(dbsession):
    from autonomie.models.task.task import TaskLineGroup
    group = TaskLineGroup(
        order=1,
        title=u"Group title",
        description=u"Group description",
    )
    dbsession.add(group)
    dbsession.flush()
    return group


@pytest.fixture
def task_line(dbsession, unity, tva, product, task_line_group):
    from autonomie.models.task.task import TaskLine
    line = TaskLine(
        cost=1250000,
        quantity=1,
        unity=unity.label,
        tva=20.0,
        product_id=product.id,
        group=task_line_group,
    )
    dbsession.add(line)
    dbsession.flush()
    return line


@pytest.fixture
def payment_line(dbsession):
    from autonomie.models.task.estimation import PaymentLine
    payment_line = PaymentLine(
        amount=1250000,
        description=u"Payment Line",
    )
    dbsession.add(payment_line)
    dbsession.flush()
    return payment_line


@pytest.fixture
def estimation(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    from autonomie.models.task.estimation import Estimation
    estimation = Estimation(
        company=company,
        project=project,
        customer=customer,
        phase=phase,
        user=user,
    )
    dbsession.add(estimation)
    dbsession.flush()
    return estimation
