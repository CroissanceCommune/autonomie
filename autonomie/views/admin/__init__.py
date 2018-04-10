# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
from autonomie.views.admin.tools import BaseAdminIndexView

BASE_URL = u"/admin"


class AdminIndexView(BaseAdminIndexView):
    title = u"Configuration de votre instance Autonomie"
    route_name = BASE_URL
    children = []


def add_admin_view(config, *args, **kwargs):
    if 'renderer' not in kwargs:
        kwargs['renderer'] = 'autonomie:templates/admin/base_view.mako'
    if 'permission' not in kwargs:
        kwargs['permission'] = 'admin'

    if 'layout' not in kwargs:
        kwargs['layout'] = 'admin'

    if 'parent' in kwargs:
        parent = kwargs.pop('parent')
        print(parent)
        parent.add_child(args[0])

    if 'route_name' not in kwargs:
        kwargs['route_name'] = args[0].route_name

    config.add_view(*args, **kwargs)


def includeme(config):
    config.include('.layout')
    config.add_directive('add_admin_view', add_admin_view)
    config.add_route(BASE_URL, BASE_URL)
    config.add_admin_view(AdminIndexView)

    config.include(".main")
    config.include(".accompagnement")
