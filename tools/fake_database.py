from autonomie.models import DBSESSION
from autonomie.models.user import User, ADMIN_PRIMARY_GROUP, \
        MANAGER_PRIMARY_GROUP, CONTRACTOR_PRIMARY_GROUP
from autonomie.models.company import Company

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
                    firstname=login,
                    lastname="FIRSTNAME_%s" % login)


def add_simple_admin(login):
    return add_simple(login, ADMIN_PRIMARY_GROUP)


def add_simple_manager(login):
    return add_simple(login, MANAGER_PRIMARY_GROUP)


def add_simple_contractor(login):
    return add_simple(login, CONTRACTOR_PRIMARY_GROUP)


def add_company(user, company_name, goal=""):
    company = Company()
    company.name = company_name
    company.goal = u"Entreprise de %s" % user.login

    user.companies.append(company)

    session = DBSESSION()
    session.add(company)

    session.flush()

    print "Added company for %s: %s" % (user.login, company_name)

    return company


def fake_database_fill():
    # Adding admins
    add_simple_admin("admin1")

    # Adding managers
    add_simple_manager("manager1")

    # Adding contractors
    contractor1 = add_simple_contractor("contractor1")

    # Adding companies
    add_company(contractor1, "IKEA")
