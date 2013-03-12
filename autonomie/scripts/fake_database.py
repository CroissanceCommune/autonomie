#-*-coding:utf-8-*-
"""
    Script for populating a fake database
"""
from autonomie.models import DBSESSION
from autonomie.models.user import User, ADMIN_PRIMARY_GROUP, \
        MANAGER_PRIMARY_GROUP, CONTRACTOR_PRIMARY_GROUP
from autonomie.models.company import Company
from autonomie.models.project import Project
from autonomie.models.project import Phase
from autonomie.models.client import Client
from autonomie.models.task.invoice import PaymentMode
from autonomie.models.tva import Tva
from autonomie.scripts.utils import command
from autonomie.models.task.unity import WorkUnit
from autonomie.models.treasury import ExpenseKmType
from autonomie.models.treasury import ExpenseTelType
from autonomie.models.treasury import ExpenseType

GROUPS = {
    ADMIN_PRIMARY_GROUP: "admin",
    MANAGER_PRIMARY_GROUP: "manager",
    CONTRACTOR_PRIMARY_GROUP: "contractor"
}


def add_user(login, password, group, firstname="", lastname=""):
    user = User(login=login, firstname=firstname, lastname=lastname)
    user.set_password(password)

    user.primary_group = group

    session = DBSESSION()
    session.add(user)

    session.flush()

    group_name = GROUPS[group]
    print "Added %s: %s/%s" % (group_name, login, password)

    return user


def add_simple(login, group):
    return add_user(login, login, group,
                    firstname=u"FIRSTNAME_%s" % login,
                    lastname=u"LASTNAME_%s" % login)


def add_simple_admin(login):
    return add_simple(login, ADMIN_PRIMARY_GROUP)


def add_simple_manager(login):
    return add_simple(login, MANAGER_PRIMARY_GROUP)


def add_simple_contractor(login):
    return add_simple(login, CONTRACTOR_PRIMARY_GROUP)


def add_company(user, company_name, goal=""):
    company = Company()
    company.name = company_name
    company.goal = goal or u"Entreprise de %s" % user.login

    user.companies.append(company)

    session = DBSESSION()
    session.add(company)

    session.flush()

    print "Added company for %s: %s" % (user.login, company_name)

    return company

def add_client(company, client_name, client_code, client_lastname):
    client = Client()
    client.name = client_name #u"Institut médical Dupont & Dupond"
    client.contactLastName = client_lastname # "Dupont"
    client.code = client_code #"IMDD"
    client.company = company

    session = DBSESSION()
    session.add(client)
    session.flush()

    print u"Added client to %s: %s" % (company.name, client_name)
    return client

def add_project(client, company, project_name, project_code):
    project = Project(name=project_name, code=project_code)
    project.clients.append(client)
    project.company = company

    session = DBSESSION()
    session.add(project)
    session.flush()

    print u"Added project to %s for %s: %s" % (company.name, client.name,
                                                            project_name)
    return project


def add_phase(project, phase_name):
    phase = Phase(name=phase_name)
    phase.project = project

    session = DBSESSION()
    session.add(phase)
    session.flush()

    print u"Added phase to %s: %s" % (project.name, phase_name)

    return phase


def add_payment_mode(label):
    p = PaymentMode(label=label)
    session = DBSESSION()
    session.add(p)
    session.flush()


def add_tva(value, default=0):
    t = Tva(name="%s %%" % (value/100.0), value=value, default=default)
    session = DBSESSION()
    session.add(t)
    session.flush()

def add_unity(label):
    t = WorkUnit(label=label)
    session = DBSESSION()
    session.add(t)
    session.flush()

def add_expense_type(type_, **kwargs):
    if type_ == 'km':
        e = ExpenseKmType(**kwargs)
    elif type_ == 'tel':
        e = ExpenseTelType(**kwargs)
    else:
        e = ExpenseType(**kwargs)
    session = DBSESSION()
    session.add(e)
    session.flush()

def set_configuration():
    add_payment_mode(u"par chèque")
    add_payment_mode(u"par virement")

    add_tva(0)
    add_tva(700)
    add_tva(1960, 1)

    add_unity(u"heure(s)")
    add_unity(u"jour(s)")
    add_unity(u"mois")
    add_unity(u"forfait")

    add_expense_type("", label=u"Restauration", code='0001')
    add_expense_type("", label=u"Transport", code='0002')
    add_expense_type("", label=u"Matériel", code="0003")
    add_expense_type("km", label=u"Scooter", code="0004", amount='0.124')
    add_expense_type("km", label=u"Voiture", code="0005", amount="0.235")
    add_expense_type("tel", label=u"Adsl-Tel fix", code="0006", percentage="80")
    add_expense_type("tel", label=u"Mobile", code="0007", percentage="80")


def fake_database_fill(arguments):
    set_configuration()
    # Adding admins
    add_simple_admin("admin1")

    # Adding managers
    add_simple_manager("manager1")

    # Adding contractors
    contractor1 = add_simple_contractor("contractor1")

    # Adding companies
    company = add_company(contractor1, u"Laveur de K-ro", u"Nettoyage de vitre")
    client = add_client(company, u"Institut médical Dupont & Dupond", "IMDD",
                                                                    "Dupont" )
    project = add_project(client, company, u"Vitrine rue Neuve", "VRND")
    phase = add_phase(project, u"Default")


def populate_fake():
    """Populate the database with fake datas
    Usage:
        autonomie-fake <config_uri> populate

    Options:
        -h --help     Show this screen.
    """
    try:
        return command(fake_database_fill, populate_fake.__doc__)
    finally:
        pass
