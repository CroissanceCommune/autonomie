# -*- coding: utf-8 -*-
# * File Name : security.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : mar. 28 août 2012 01:06:51 CEST
#
# * Project : autonomie
#
"""
    Root factory <=> Acl handling
"""
import logging
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import DENY_ALL
from sqlalchemy.orm import undefer_group

from autonomie.models.model import Project
from autonomie.models.model import Company
from autonomie.models.model import Client
from autonomie.models.model import Estimation
from autonomie.models.model import Invoice
from autonomie.models.model import CancelInvoice
from autonomie.models.model import User
from autonomie.models.model import OperationComptable

log = logging.getLogger(__name__)

DEFAULT_PERM = [(Allow, "group:admin", ALL_PERMISSIONS,),
                (Allow, "group:manager", ("manage", "add", "edit", "view")),
                ]

def wrap_db_objects():
    """
        Add acls and names to the db objects used as context
    """
    Company.__acl__ = property(get_company_acl)
    Project.__acl__ = property(get_client_or_project_acls)
    Client.__acl__ = property(get_client_or_project_acls)
    Estimation.__acl__ = property(get_task_acl)
    Invoice.__acl__ = property(get_task_acl)
    CancelInvoice.__acl__ = property(get_task_acl)
    User.__acl__ = property(get_user_acl)
    OperationComptable.__acl__ = property(get_task_acl)

class BaseDBFactory(object):
    """
        Base class for dbrelated objects
    """
    __acl__ = DEFAULT_PERM[:]
    dbsession = None

class RootFactory(dict):
    """
       Ressource factory, returns the appropriate resource regarding
       the request object
    """
    __name__ = "root"

    @property
    def __acl__(self):
        """
            Default permissions
        """
        #log.debug("# Getting root acls : ")
        acl = DEFAULT_PERM[:]
        acl.append((Allow, Authenticated, 'view',))
        #log.debug(acl)
        return acl

    def __init__(self, request):
        self.request = request
        self['companies'] = CompanyFactory(self, "companies")
        self['projects'] = ProjectFactory(self, 'projects')
        self['clients'] = ClientFactory(self, 'clients')
        self['estimations'] = EstimationFactory(self, 'estimations')
        self['invoices'] = InvoiceFactory(self, 'invoices')
        self['cancelinvoices'] = CancelInvoiceFactory(self, 'cancelinvoices')
        self['users'] = UserFactory(self, 'users')
        self['operations'] = OperationFactory(self, 'operations')


def get_company_acl(self):
    """
        Compute the company's acls
    """
    acl = DEFAULT_PERM[:]
    acl.append((Allow, Authenticated, 'view',))
    acl.extend([(Allow, u"%s" % user.login, ("view", "edit", "add"))
                        for user in self.employees])
    return acl

class CompanyFactory(BaseDBFactory):
    """
        Handle access to a project
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(Company).options(undefer_group('edit')).filter(
                               Company.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'company'
        return obj

def get_client_or_project_acls(self):
    """
        Compute the project's acls
    """
    acl = DEFAULT_PERM[:]
    acl.extend([(Allow, u"%s" % user.login, ("view", "edit", "add"))
                        for user in self.company.employees])
    #log.debug("# Getting acls for the current project or client : ")
    #log.debug(acl)
    return acl

class ProjectFactory(BaseDBFactory):
    """
        Handle access to a project
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(Project).options(undefer_group('edit')).filter(
                                               Project.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'project'
        return obj

class ClientFactory(BaseDBFactory):
    """
        Handle access to a client
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(Client).options(undefer_group('edit')).filter(
                                             Client.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'client'
        return obj

def get_task_acl(self):
    """
        return the acls of the current task object
    """
    acl = DEFAULT_PERM[:]
    acl.extend([(Allow, u"%s" % user.login, ("view", "edit", "add"))
                        for user in self.project.company.employees])
    #log.debug("# Getting acls for the current task : ")
    #log.debug(acl)
    return acl

class EstimationFactory(BaseDBFactory):
    """
        Handle access to a client
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(Estimation).options(undefer_group('edit')).filter(
                                           Estimation.IDTask==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'estimation'
        return obj

class InvoiceFactory(BaseDBFactory):
    """
        Handle access to an invoice
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(Invoice).options(undefer_group('edit')).filter(
                                             Invoice.IDTask==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'invoice'
        return obj


class CancelInvoiceFactory(BaseDBFactory):
    """
        Handle access to a cancelinvoice
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(CancelInvoice).options(undefer_group('edit')
                                  ).filter(CancelInvoice.IDTask==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'cancelinvoice'
        return obj

def get_user_acl(self):
    """
        Get acls for user account edition
    """
    acl = DEFAULT_PERM[:]
    acl.append((Allow, u"%s" % self.login, ("view", "edit", "add")))
    acl.append((Allow, Authenticated, ('view')))
    return acl

class UserFactory(BaseDBFactory):
    """
        Handle access to a user account
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(User).options(undefer_group('edit')
                                            ).filter(User.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'user'
        return obj

def get_base_acl(self):
    """
        return the base acls
    """
    acl = DEFAULT_PERM[:]
    return acl

class OperationFactory(BaseDBFactory):
    """
        Handle access to a comptability operation entry
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        #log.debug("We are in the __getitem__")
        #log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        obj = dbsession.query(OperationComptable).options(
                undefer_group('edit')).filter(
                                OperationComptable.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__name__ = 'operation'
        return obj
