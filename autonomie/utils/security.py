# -*- coding: utf-8 -*-
# * File Name : security.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : lun. 11 juin 2012 16:19:34 CEST
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

from autonomie.models.model import Project
from autonomie.models.model import Company
from autonomie.models.model import Client
from autonomie.models.model import Estimation
from autonomie.models.model import Invoice
from autonomie.models.model import User

log = logging.getLogger(__file__)

DEFAULT_PERM = [(Allow, "group:admin", ALL_PERMISSIONS,),
                (Allow, Authenticated, 'view'),]

class BaseDBFactory(object):
    """
        Base class for dbrelated objects
    """
    acl = DEFAULT_PERM[:]
    dbsession = None

class RootFactory(dict):
    """
       Ressource factory, returns the appropriate resource regarding
       the request object
    """
    __name__ = "root"
    __acl__ = DEFAULT_PERM[:]

    def __init__(self, request):
        self.request = request
        self['companies'] = CompanyFactory(self, "companies")
        self['projects'] = ProjectFactory(self, 'projects')
        self['clients'] = ClientFactory(self, 'clients')
        self['estimations'] = EstimationFactory(self, 'estimations')
        self['invoices'] = InvoiceFactory(self, 'invoices')
        self['users'] = UserFactory(self, 'users')


def get_company_acl(self):
    """
        Compute the company's acls
    """
    acl = DEFAULT_PERM[:]
    acl.extend([(Allow, u"%s" % user.login, ("view", "edit",))
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
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        Company.__acl__ = property(get_company_acl)
        obj = dbsession.query(Company).filter(
                               Company.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "company"
        return obj

def get_client_or_project_acls(self):
    """
        Compute the project's acls
    """
    acl = DEFAULT_PERM[:]
    acl.extend([(Allow, u"%s" % user.login, ("view", "edit",))
                        for user in self.company.employees])
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
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        Project.__acl__ = property(get_client_or_project_acls)
        obj = dbsession.query(Project).filter(
                                               Project.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "project"
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
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        Client.__acl__ = property(get_client_or_project_acls)
        obj = dbsession.query(Client).filter(
                                             Client.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "client"
        return obj

def get_task_acl(self):
    """
        return the acls of the current task object
    """
    acl = DEFAULT_PERM[:]
    acl.extend([(Allow, u"%s" % user.login, ("view", "edit",))
                        for user in self.project.company.employees])
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
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        dbsession = self.dbsession()
        Estimation.__acl__ = property(get_task_acl)
        obj = dbsession.query(Estimation).filter(
                                           Estimation.IDTask==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "estimation"
        return obj

class InvoiceFactory(BaseDBFactory):
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
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        Invoice.__acl__ = property(get_task_acl)
        dbsession = self.dbsession()
        obj = dbsession.query(Invoice).filter(
                                             Invoice.IDTask==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "invoice"
        return obj

def get_user_acl(self):
    """
        Get acls for user account edition
    """
    acl = DEFAULT_PERM[:]
    acl.append((Allow, u"%s" % self.login, ("view", "edit",)))
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
        log.debug("We are in the __getitem__")
        log.debug(key)
        if self.dbsession == None:
            raise Exception("Missing dbsession")
        User.__acl__ = property(get_task_acl)
        dbsession = self.dbsession()
        obj = dbsession.query(User).filter(User.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "user"
        return obj
