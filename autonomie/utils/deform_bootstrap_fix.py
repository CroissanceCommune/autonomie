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
    Hack for https://github.com/Kotti/deform_bootstrap/issues/41
    Copy of : https://github.com/Kotti/deform_bootstrap/pull/44
"""
from deform import Form
from deform.widget import FormWidget

default_resources = {
        "chosen":{None:{'js':("jquery_chosen/chosen.jquery.js",),
                        'css':("jquery_chosen/chosen.css",
                                "chosen_bootstrap.css",)}
                 },
        "bootstrap":{None:{'js':'bootstrap.min.js',
                           'css':'deform_bootstrap.css'}},
        }

def add_resources_to_registry():
    """
        Register deform_bootstrap widget specific requirements to deform's
        default resource registry
    """
    registry = Form.default_resource_registry
    for rqrt, versions in default_resources.items():
        for version, resources in versions.items():
            registry.set_js_resources(rqrt, version, resources.get('js'))
            registry.set_css_resources(rqrt, version, resources.get('css'))
