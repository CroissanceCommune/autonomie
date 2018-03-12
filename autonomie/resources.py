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
from js.bootstrap import (
    bootstrap_css,
    bootstrap,
)
from js.jquery import jquery
from js.jqueryui import effects_highlight
from js.jqueryui import effects_shake
from js.jqueryui import ui_dialog
from js.jqueryui import ui_sortable
from js.jqueryui import ui_datepicker_fr
from js.jqueryui import bootstrap as jqueryui_bootstrap_theme
from js.jquery_timepicker_addon import timepicker_js
from js.jquery_form import jquery_form
from js.jquery_qunit import jquery_qunit
from js.select2 import select2
from js.tinymce import tinymce

lib_autonomie = Library("fanstatic", "static")


def get_resource(filepath, minified=None, depends=None, bottom=False):
    """
    Return a resource object included in autonomie
    """
    return Resource(
        lib_autonomie,
        filepath,
        minified=minified,
        depends=depends,
        bottom=bottom,
    )


# Css resources
font_awesome_css = get_resource("css/font-awesome.min.css")
main_css = get_resource(
    "css/main.css",
    depends=[
        bootstrap_css,
        jqueryui_bootstrap_theme,
        font_awesome_css,
    ]
)
opa_css = get_resource("css/opa.css", depends=[main_css])
opa_vendor_js = get_resource(
    'js/build/vendor.bundle.js',
    minified='js/build/vendor.min.js',
    bottom=True,
)
base_setup_js = get_resource(
    'js/build/base_setup.js',
    minified='js/build/base_setup.min.js',
    depends=(opa_vendor_js,),
    bottom=True,
)

# Js static resources
_date = get_resource("js/date.js")
_math = get_resource("js/math.js")
_dom = get_resource("js/dom.js", depends=[jquery])


def get_opa_group():
    """
    Return the resources used on one page applications pages
    """
#    js_tools = Group([_date])
    return Group([main_css, opa_css, opa_vendor_js, base_setup_js])


def get_main_group():
    """
    Return the main resource Group that will be used on all pages
    """
    # UnPackaged external libraries
    underscore = get_resource(
        "js/vendors/underscore.js",
        minified="js/vendors/underscore-min.js"
    )

    main_js = get_resource(
        "js/main.js",
        depends=[
            ui_dialog, ui_sortable, underscore, timepicker_js, bootstrap,
            _math,
        ]
    )

    js_tools = Group([main_js, _dom, _math, _date, select2])

    return Group([
        main_css,
        js_tools,
        jquery_form,
        ui_datepicker_fr,
    ])


main_group = get_main_group()
opa_group = get_opa_group()


jstree_js = get_resource(
    "js/vendors/jstree.js",
    minified="js/vendors/jstree.min.js",
    depends=[main_group]
)
jstree_css = get_resource("css/jstree_themes/default/style.css")
jstree = Group([jstree_js, jstree_css])


def get_module_group():
    """
    Return main libraries used in custom modules (backbone marionette and
    handlebar stuff)

    NB : depends on the main_group
    """
    handlebar = get_resource("js/vendors/handlebars.runtime.js")
    backbone = get_resource(
        "js/vendors/backbone.js",
        minified="js/vendors/backbone-min.js",
        depends=[main_group],
    )
    backbone_marionnette = get_resource(
        "js/vendors/backbone.marionette.js",
        minified="js/vendors/backbone.marionette.min.js",
        depends=[backbone]
    )
    # Bootstrap form validation stuff
    backbone_validation = get_resource(
        "js/vendors/backbone-validation.js",
        minified="js/vendors/backbone-validation-min.js",
        depends=[backbone]
    )
    backbone_validation_bootstrap = get_resource(
        "js/backbone-validation-bootstrap.js",
        depends=[backbone_validation]
    )
    # Popup object
    backbone_popup = get_resource(
        "js/backbone-popup.js",
        depends=[backbone_marionnette]
    )
    # Some specific tuning
    backbone_tuning = get_resource(
        "js/backbone-tuning.js",
        depends=[backbone_marionnette, handlebar]
    )
    # The main templates
    main_templates = get_resource(
        "js/template.js",
        depends=[handlebar]
    )
    # Messages
    message_js = get_resource(
        "js/message.js",
        depends=[handlebar]
    )
    return Group(
        [
            backbone_marionnette,
            backbone_validation_bootstrap,
            backbone_tuning,
            backbone_popup,
            main_templates,
            effects_highlight,
            effects_shake,
            message_js,
        ]
    )


module_libs = get_module_group()


def get_module_resource(module, tmpl=False, extra_depends=()):
    """
    Return a resource group (or a single resource) for the given module

    static/js/<module>.js and static/js/templates/<module>.js

    :param str module: the name of a js file
    :param bool tmpl: is there an associated tmpl
    :param extra_depends: extra dependencies
    """
    depends = [module_libs]
    depends.extend(extra_depends)
    if tmpl:
        tmpl_resource = get_resource(
            "js/templates/%s.js" % module,
            depends=[module_libs]
        )
        depends.append(tmpl_resource)

    return get_resource(
        "js/%s.js" % module,
        depends=depends
    )


discount = get_module_resource("discount", extra_depends=[jstree])
address = get_module_resource("address")
tva = get_module_resource("tva")

task_list_js = get_module_resource("task_list")
task_add_js = get_module_resource("task_add")
estimation_signed_status_js = get_module_resource("estimation_signed_status")
event_list_js = get_module_resource('event_list')

job_js = get_module_resource("job", tmpl=True)

statistics_js = get_module_resource(
    'statistics',
    tmpl=True,
    extra_depends=[select2]
)
competence_js = get_module_resource(
    'competence',
    tmpl=True,
    extra_depends=[select2]
)
sale_product_js = get_module_resource(
    'sale_product',
    tmpl=True,
    extra_depends=[select2, tinymce]
)
holiday_js = get_module_resource("holiday", tmpl=True)
commercial_js = get_module_resource("commercial")

pdf_css = get_resource('css/pdf.css', depends=[main_group])
# Permet d'overrider ou compléter les css de la sortie pdf pour l'affichage html
task_html_pdf_css = get_resource('css/task_pdf.css')


# Test tools
def get_test_resource():
    res = []
    for i in ('math', 'date', 'dom'):
        res.append(
            get_resource(
                "js/tests/test_%s.js" % i,
                depends=(jquery_qunit, main_group)
            )
        )
    return Group(res)


test_js = get_test_resource()

# File upload page js requirements
fileupload_js = get_resource(
    "js/fileupload.js",
    depends=[main_group],
)

# Chart tools
d3_js = get_resource("js/vendors/d3.v3.js", minified="js/vendors/d3.v3.min.js")
radar_chart_js = get_resource("js/vendors/radar-chart.js", depends=[d3_js])
radar_chart_css = get_resource(
    "css/radar-chart.css",
    minified="css/radar-chart.min.css"
)
competence_radar_js = get_module_resource(
    "competence_radar", extra_depends=(radar_chart_js, radar_chart_css,)
)

admin_expense_js = get_module_resource("admin_expense")

# Task form resources
task_css = get_resource('css/task.css', depends=(opa_css, ))
task_js = get_resource(
    'js/build/task.js',
    minified='js/build/task.min.js',
    depends=[opa_vendor_js],
    bottom=True,
)
task_resources = Group([task_js, task_css, jstree_css])

# Expense form resources
expense_css = get_resource('css/expense.css', depends=(opa_css, ))
expense_js = get_resource(
    'js/build/expense.js',
    minified='js/build/expense.min.js',
    depends=[opa_vendor_js],
    bottom=True,
)
expense_resources = Group([expense_js, expense_css])

# User page related resources
user_css = get_resource('css/user.css', depends=(main_css, ))
user_resources = Group([user_css, main_group])
