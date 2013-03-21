# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 14-01-2013
# * Last Modified :
#
# * Project :
#
"""
    Handle static libraries inside autonomie with the help of fanstatic
"""
import fanstatic
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.bootstrap import bootstrap
from js.bootstrap import bootstrap_responsive_css
from js.jquery import jquery
from js.jqueryui import ui_dialog
from js.jqueryui import ui_sortable
from js.jqueryui import ui_autocomplete
from js.jqueryui import ui_datepicker_fr
from js.jquery_maskedinput import jquery_maskedinput
from js.jquery_form import jquery_form
from js.deform_bootstrap import deform_bootstrap_js
from js.chosen import chosen_jquery
from js.jquery_qunit import jquery_qunit

lib_autonomie = Library("fanstatic", "static")

main = Resource(lib_autonomie, "js/main.js", depends=[ui_dialog, ui_sortable])

_hogan = Resource(lib_autonomie, "js/hogan-2.0.0.js")
_underscore = Resource(lib_autonomie, "js/underscore.js",
        minified="js/underscore-min.js")
_backbone = Resource(lib_autonomie, "js/backbone.js",
        minified="js/backbone-min.js", depends=[_underscore])
_backbone_marionnette = Resource(lib_autonomie, "js/backbone.marionette.js",
        minified="js/backbone.marionette.min.js", depends=[_backbone])
_backbone_validation = Resource(lib_autonomie, "js/backbone-validation.js",
        minified="js/backbone-validation-min.js", depends=[_backbone])

_backbone_tuning = Resource(lib_autonomie, "js/backbone-tuning.js",
        depends=[_backbone_marionnette, _hogan, main])
_backbone_validation_bootstrap = Resource(lib_autonomie,
        "js/backbone-validation-bootstrap.js", depends=[_backbone_validation])
_backbone_popup = Resource(lib_autonomie,
        "js/backbone-popup.js", depends=[_backbone_marionnette]);

backbone = Group([_backbone_validation_bootstrap,
                  _backbone_tuning, _backbone_popup])

templates = Resource(lib_autonomie,
        "js/template.js", depends=[_hogan])
jquery_tmpl = Resource(lib_autonomie, "js/jquery.tmpl.min.js",
                  depends=[jquery])


_date = Resource(lib_autonomie, "js/date.js")
_dom = Resource(lib_autonomie, "js/dom.js", depends=[jquery])
_math = Resource(lib_autonomie, "js/math.js")
tools = Group([_dom, _math, _date])


duplicate = Resource(lib_autonomie, "js/duplicate.js", depends=[jquery])
discount = Resource(lib_autonomie, "js/discount.js", depends=[backbone])
address = Resource(lib_autonomie, "js/address.js", depends=[jquery])
task = Resource(lib_autonomie, "js/task.js",
        depends=[tools, jquery_tmpl, address, discount, duplicate, backbone,
            templates])

# Main javascript requirements
main_js = Group([main,
                 bootstrap,
                 bootstrap_responsive_css,
                 jquery_form,
                 ui_autocomplete,
                 ui_datepicker_fr,
                 jquery_maskedinput,
                 deform_bootstrap_js,
                 chosen_jquery])
# Javascript requirements for task pages/forms
task_js = Group([main,
                 bootstrap,
                 bootstrap_responsive_css,
                 jquery_form,
                 ui_datepicker_fr,
                 deform_bootstrap_js,
                 task])

# Test tools
test_js = Group([main,
                 bootstrap,
                 bootstrap_responsive_css,
                 jquery_form,
                 ui_datepicker_fr,
                 deform_bootstrap_js,
                 task,
                 jquery_qunit])
