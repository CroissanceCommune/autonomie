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
from js.bootstrap import bootstrap_js
from js.jquery import jquery
from js.jqueryui import ui_dialog
from js.jqueryui import ui_datepicker_fr
#from js.jqueryui import bootstrap as jqueryui_bootstrap_theme
from js.jquery_form import jquery_form
from js.deform_bootstrap import deform_bootstrap_js
from js.chosen import chosen_jquery

lib_autonomie = Library("fanstatic", "static")

main = Resource(lib_autonomie, "js/main.js", depends=[ui_dialog])

underscore = Resource(lib_autonomie, "js/underscore.js",
        minified="js/underscore-min.js")
backbone = Resource(lib_autonomie, "js/backbone.js",
        minified="js/backbone-min.js",
        depends=[underscore])
backbone_marionnette = Resource(lib_autonomie, "js/backbone.marionette.js",
        minified="js/backbone.marionette.min.js",
        depends=[backbone])

dom = Resource(lib_autonomie, "js/dom.js", depends=[jquery])
duplicate = Resource(lib_autonomie, "js/duplicate.js", depends=[jquery])
jquery_maskedinput = Resource(lib_autonomie, "js/jquery.maskedinput-1.3.min.js",
        depends=[jquery])
jquery_tmpl = Resource(lib_autonomie, "js/jquery.tmpl.min.js",
        depends=[jquery])
discount = Resource(lib_autonomie, "js/discount.js",
        depends=[backbone_marionnette])
address = Resource(lib_autonomie, "js/address.js")
date = Resource(lib_autonomie, "js/date.js")
task = Resource(lib_autonomie, "js/task.js", depends=[date, jquery_tmpl,
                            address, discount, duplicate, dom])

# Main javascript requirements
main_js = Group([main,
                 bootstrap_js,
                 jquery_form,
                 ui_datepicker_fr,
                 jquery_maskedinput,
                 deform_bootstrap_js,
                 chosen_jquery])
# Javascript requirements for task pages/forms
task_js = Group([main,
                 bootstrap_js,
                 jquery_form,
                 ui_datepicker_fr,
                 deform_bootstrap_js,
                 task])
