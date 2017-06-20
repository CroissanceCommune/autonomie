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

"""
    Script for populating a fake database
"""
import sys

from autonomie_base.models.base import DBSESSION
from autonomie.models.user import User, ADMIN_PRIMARY_GROUP, \
        MANAGER_PRIMARY_GROUP, CONTRACTOR_PRIMARY_GROUP
from autonomie.models.company import Company
from autonomie.models.project import Project
from autonomie.models.project import Phase
from autonomie.models.customer import Customer
from autonomie.models.task.invoice import PaymentMode
from autonomie.models.tva import Tva
from autonomie.scripts.utils import command
from autonomie.models.task.unity import WorkUnit
from autonomie.models.expense import (
    ExpenseKmType,
    ExpenseTelType,
    ExpenseType,
)
from autonomie.models.activity import (
    ActivityType,
    ActivityMode,
    ActivityAction,
)

GROUPS = {
    ADMIN_PRIMARY_GROUP: "admin",
    MANAGER_PRIMARY_GROUP: "manager",
    CONTRACTOR_PRIMARY_GROUP: "contractor"
}


def add_user(login, password, group, firstname="", lastname="", email=""):
    user = User(login=login,
                firstname=firstname,
                lastname=lastname,
                email=email)
    user.set_password(password)

    user.groups.append(GROUPS[group])

    session = DBSESSION()
    session.add(user)

    session.flush()

    group_name = GROUPS[group]
    print "Added %s: %s/%s" % (group_name, login, password)

    return user


def add_simple(login, group):
    return add_user(login, login, group,
                    firstname=u"FIRSTNAME_%s" % login,
                    lastname=u"LASTNAME_%s" % login,
                   email="%s@example.com" % login)


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

def add_customer(**kw): #company, customer_name, customer_code, customer_lastname):
    customer = Customer(**kw)

    session = DBSESSION()
    session.add(customer)
    session.flush()

    print u"Added customer to %s: %s" % (
        customer.company.name,
        customer.name)
    return customer

def add_project(customer, company, project_name, project_code):
    project = Project(name=project_name, code=project_code)
    project.customers.append(customer)
    project.company = company

    session = DBSESSION()
    session.add(project)
    session.flush()

    print u"Added project to %s for %s: %s" % (company.name, customer.name,
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


def add_tva(value, default=False):
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

def add_activity_type(label):
    session = DBSESSION()
    session.add(ActivityType(label=label))
    session.flush()

def add_activity_mode(label):
    session = DBSESSION()
    session.add(ActivityMode(label=label))
    session.flush()

def add_activity_action(label, **kw):
    session = DBSESSION()
    a = ActivityAction(label=label, **kw)
    session.add(a)
    session.flush()
    return a


def set_configuration():
    print("Adding configuration elements")
    add_payment_mode(u"par chèque")
    add_payment_mode(u"par virement")

    add_tva(0)
    add_tva(700)
    add_tva(1960, True)

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

    for i in (u'Rendez-vous mensuel', u'Entretien individuel'):
        add_activity_type(i)

    for i in (u'par skype', u'en direct', u'par mail', u'par téléphone', ):
        add_activity_mode(i)

    a = add_activity_action(
        u"Projet FSE 2014 - Passerelle pour l'entreprenariat collectif",)
    add_activity_action(
        u"Module 3 : Accompagnement renforcé - Etape : Business model \
commercial, économique et social", parent=a)

    session = DBSESSION()
    from autonomie.models import initialize
    initialize.populate_situation_options(session)
    initialize.populate_groups(session)



def fake_database_fill():

    # Adding admins
    add_simple_admin("admin1")

    # Adding managers
    add_simple_manager("manager1")

    # Adding contractors
    contractor1 = add_simple_contractor("contractor1")

    # Adding companies
    company = add_company(
        contractor1,
        u"Laveur de K-ro",
        u"Nettoyage de vitre",
    )
    customer = add_customer(
        company=company,
        name=u"Institut médical Dupont & Dupond",
        code="IMDD",
        lastname="Dupont",
        address=u"Avenue Victor Hugo",
        zip_code=u"21000",
        city=u"Dijon"
    )
    project = add_project(customer, company, u"Vitrine rue Neuve", "VRND")
    phase = add_phase(project, u"Default")


def populate_fake():
    """Populate the database with fake datas
    Usage:
        autonomie-fake <config_uri> populate
        autonomie-fake <config_uri> populate_conf

    Options:
        -h --help     Show this screen.
    """
    def callback(arguments, env):
        if arguments['populate']:
            func = fake_database_fill
        elif arguments['populate_conf']:
            func = set_configuration
        else:
            print populate_fake.__doc__
            sys.exit(1)
        return func()
    try:
        return command(callback, populate_fake.__doc__)
    finally:
        pass
