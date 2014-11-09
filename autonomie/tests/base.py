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
class Dummy(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def printstatus(obj):
    """
        print an object's status regarding the sqla's session
    """
    from sqlalchemy.orm import object_session
    from sqlalchemy.orm.util import has_identity
    if object_session(obj) is None and not has_identity(obj):
        print "Sqlalchemy status : transient"
    elif object_session(obj) is not None and not has_identity(obj):
        print "Sqlalchemy status : pending"
    elif object_session(obj) is None and has_identity(obj):
        print "Sqlalchemy status : detached"
    elif object_session(obj) is not None and has_identity(obj):
        print "Sqlalchemy status : persistent"
    else:
        print "Unknown Status"

