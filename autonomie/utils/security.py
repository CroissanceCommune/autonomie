# -*- coding: utf-8 -*-
# * File Name : security.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : mar. 05 juin 2012 23:48:10 CEST
#
# * Project : autonomie
#
"""
    Root factory <=> Acl handling
"""
import logging
from pyramid.security import Allow
from pyramid.security import Authenticated

from autonomie.models.model import Project
from autonomie.models.model import Company
from autonomie.models.model import Client

log = logging.getLogger(__file__)

class BaseDBFactory(object):
    __acl__ = [(Allow, Authenticated, 'view'),]
    dbsession = None

class RootFactory(dict):
    """
       Ressource factory, returns the appropriate resource regarding
       the request object
    """
    __acl__ = [
                (Allow, Authenticated, 'view'),
                ]
    def __init__(self, request):
        self.request = request
        self['companies'] = CompanyFactory(self, "companies")
        self['projects'] = ProjectFactory(self, 'projects')
        self['clients'] = ClientFactory(self, 'clients')

class CompanyWrapper(Company):
    """
        Wrap The project model to handle acls
    """
    @property
    def __acl__(self):
        acl = [(Allow, u"admin", ("view", 'edit',)),
               (Allow, Authenticated, ('visit',)),]
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
        obj = dbsession.query(CompanyWrapper).filter(
                               CompanyWrapper.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "company"
        return obj

class ProjectWrapper(Project):
    """
        Wrap The project model to handle acls
    """
    @property
    def __acl__(self):
        acl = [(Allow, u"admin", ("view", 'edit',)),]
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
        obj = dbsession.query(ProjectWrapper).filter(
                                               ProjectWrapper.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "project"
        return obj

class ClientWrapper(Client):
    """
        Wrap The client model to handle acls
    """
    @property
    def __acl__(self):
        acl = [(Allow, u"admin", ("view", 'edit',)),]
        acl.extend([(Allow, u"%s" % user.login, ("view", "edit",))
                            for user in self.company.employees])
        return acl

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
        obj = dbsession.query(ClientWrapper).filter(
                                             ClientWrapper.id==key).scalar()
        if obj is None:
            raise KeyError
        obj.__parent__ = self
        obj.__name__ = "client"
        return obj
