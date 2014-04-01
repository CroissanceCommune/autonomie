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
    Handle static libraries inside autonomie with the help of fanstatic
"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.bootstrap import bootstrap
#from js.bootstrap import bootstrap_responsive_css
from js.jquery import jquery
from js.jqueryui import effects_highlight
from js.jqueryui import effects_shake
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

jquery_tmpl = Resource(
        lib_autonomie,
        "js/vendors/jquery.tmpl.min.js",
        depends=[jquery])
_handlebar = Resource(
        lib_autonomie,
        "js/vendors/handlebars.runtime-v1.1.2.js")
_underscore = Resource(
        lib_autonomie,
        "js/vendors/underscore.js",
        minified="js/vendors/underscore-min.js")
_backbone = Resource(
        lib_autonomie,
        "js/vendors/backbone.js",
        minified="js/vendors/backbone-min.js",
        depends=[_underscore])
_backbone_marionnette = Resource(
        lib_autonomie,
        "js/vendors/backbone.marionette.js",
        minified="js/vendors/backbone.marionette.min.js",
        depends=[_backbone])
_backbone_validation = Resource(
        lib_autonomie,
        "js/vendors/backbone-validation.js",
        minified="js/vendors/backbone-validation-min.js",
        depends=[_backbone])

_backbone_validation_bootstrap = Resource(
        lib_autonomie,
        "js/backbone-validation-bootstrap.js",
        depends=[_backbone_validation])
_backbone_popup = Resource(
        lib_autonomie,
        "js/backbone-popup.js",
        depends=[_backbone_marionnette]);

_backbone_tuning = Resource(
        lib_autonomie,
        "js/backbone-tuning.js",
        depends=[_backbone_marionnette, _handlebar, main])

backbone = Group([_backbone_validation_bootstrap,
                  _backbone_tuning, _backbone_popup])


templates = Resource(lib_autonomie,
        "js/template.js", depends=[_handlebar])

_date = Resource(
        lib_autonomie,
        "js/date.js")
_dom = Resource(
        lib_autonomie,
        "js/dom.js",
        depends=[jquery])
_math = Resource(
        lib_autonomie,
        "js/math.js")
tools = Group([_dom, _math, _date])

bootstrap_responsive_css = Resource(lib_autonomie,
        "css/bootstrap-responsive.css", depends=[bootstrap])


duplicate = Resource(
        lib_autonomie,
        "js/duplicate.js",
        depends=[jquery])
discount = Resource(
        lib_autonomie,
        "js/discount.js",
        depends=[backbone])
address = Resource(
        lib_autonomie,
        "js/address.js",
        depends=[jquery])
tva = Resource(lib_autonomie, "js/tva.js", depends=[jquery])
task = Resource(
        lib_autonomie,
        "js/task.js",
        depends=[tools, jquery_tmpl, address, discount, duplicate, backbone,
            templates, tva])
task_list_js = Resource(
        lib_autonomie,
        "js/task_list.js",
        depends=[tools, jquery, backbone])
activity_list_js = Resource(
        lib_autonomie,
        "js/activity_list.js",
        depends=[tools, jquery, backbone])
message_js = Resource(
        lib_autonomie,
        "js/message.js",
        depends=[templates, jquery])
expense_js = Resource(
        lib_autonomie,
        "js/expense.js",
        depends=[backbone, templates, tools, effects_highlight, effects_shake,
            message_js])

holiday_js = Resource(
        lib_autonomie,
        "js/holiday.js",
        depends=[backbone, templates, tools, effects_highlight, effects_shake,
            message_js])

jquery_theme_css = Resource(
        lib_autonomie,
        "css/theme/jquery-ui-1.8.16.custom.css")
main_css = Resource(
        lib_autonomie,
        "css/main.css",
        depends=[bootstrap, bootstrap_responsive_css, jquery_theme_css]
        )


# Main javascript requirements
main_js = Group([main,
                 bootstrap,
                 bootstrap_responsive_css,
                 main_css,
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

# File upload page js requirements
fileupload_js = Resource(
        lib_autonomie,
        "js/fileupload.js",
        depends=[main_js])
