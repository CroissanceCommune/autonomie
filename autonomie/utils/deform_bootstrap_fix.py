# -*- coding: utf-8 -*-
# * File Name : deform_bootstrap_fix.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 21-01-2013
# * Last Modified :
#
# * Project :
#
"""
    Hack for https://github.com/Kotti/deform_bootstrap/issues/41
    Copy of : https://github.com/Kotti/deform_bootstrap/pull/44
"""
from deform import Form

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

