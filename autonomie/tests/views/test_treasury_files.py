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
    test treasury files views
"""
import os
from mock import Mock
from pyramid.exceptions import HTTPForbidden, HTTPNotFound
from autonomie.views.treasury_files import (
    Treasury,
    isprefixed,
    code_is_not_null,
    IncomeStatement,
    SalarySheet,
    digit_subdirs,
    file_display)

CODE = "125"


#def make_directories():
#    for directory in ('tresorerie', 'resultat', 'salaire'):
#        for year in range(2010,2012):
#            for month in range(1, 13):
#                path = os.path.join(DATASDIR, directory, str(year), str(month))
#                os.system("mkdir -p %s" % path)
#                for i in range(4):
#                    fname = "%s_%s_test.pdf" % (CODE, i)
#                    fpath = os.path.join(path, fname)
#                    os.system("touch %s" % fpath)



def test_digit_subdirs(settings):
    path = os.path.join(settings['autonomie.ftpdir'], "tresorerie", "2010")
    dirs = list(digit_subdirs(path))
    assert len(dirs) == 12

def test_list_files(settings, get_csrf_request):
    path = os.path.join(settings['autonomie.ftpdir'], "tresorerie", "2010", "1")
    request = get_csrf_request()
    view = Treasury(request)
    assert len(view.list_files(path, prefix='')) == 0
    assert len(view.list_files(path, prefix='12')) == 0
    assert len(view.list_files(path, prefix=CODE+'6')) == 0
    assert len(view.list_files(path, prefix=CODE)) == 4

def test_list_files_sorted(settings, get_csrf_request):
    path = os.path.join(settings['autonomie.ftpdir'], "tresorerie", "2010", "1")
    request = get_csrf_request()
    view = Treasury(request)
    files = view.list_files(path, prefix=CODE)
    prev = files[0]
    for f_ in files[1:]:
        assert cmp(f_.name, prev.name) == 1
        prev = f_

def test_isprefixed():
    assert(isprefixed("256_bar.pdf", "256"))
    assert(isprefixed("256_bar.pdf"))
    assert(not isprefixed("256_bar.pdf", "32"))
    assert(not isprefixed("256_bar.pdf", "2567"))
    assert(not isprefixed("256_bar.pdf", "25"))

def test_code_is_not_null():
    assert(code_is_not_null("2"))
    for i in '0', '', None:
        assert(not code_is_not_null(i))

def test_view(config, get_csrf_request):
    request = get_csrf_request()
    request.context = Mock(code_compta=CODE)
    config.add_route('treasury_files', '/')
    for factory in IncomeStatement, SalarySheet, Treasury:
        view = factory(request)
        result = view.__call__()
        assert len(result['documents'].keys()) == 2
        assert len(result['documents']['2010']) == 12

def test_nutt(config, get_csrf_request):
    request = get_csrf_request()
    request.context = Mock(code_compta="")
    config.add_route('treasury_files', '/')
    for factory in IncomeStatement, SalarySheet, Treasury:
        view = factory(request)
        assert view()['documents'] == {}


def test_file(get_csrf_request):
    request = get_csrf_request(post={'name':'/resultat/2011/1/125_1_test.pdf'})
    request.context = Mock(code_compta=CODE)
    result = file_display(request)
    assert(result.content_disposition == "attachment; filename=125_1_test.pdf")
    assert(result.content_type == "application/pdf")

def test_forbidden_nocode(get_csrf_request):
    request = get_csrf_request(post={'name':'/resultat/2011/1/125_test.pdf'})
    request.context = Mock(code_compta="")
    result = file_display(request)
    assert(isinstance(result, HTTPForbidden))

def test_forbidden_wrond_code(get_csrf_request):
    request = get_csrf_request(post={'name':'/resultat/2011/1/125_test.pdf'})
    request.context = Mock(code_compta=CODE + "1")
    result = file_display(request)
    assert(isinstance(result, HTTPForbidden))

def test_forbidden_notsubdir(get_csrf_request):
    request = get_csrf_request(post={'name':'../../test/125_test.pdf'})
    request.context = Mock(code_compta=CODE)
    result = file_display(request)
    assert(isinstance(result, HTTPForbidden))

def test_notfound(get_csrf_request):
    request = get_csrf_request(post={'name':'/resultat/2011/1/125_test2.pdf'})
    request.context = Mock(code_compta=CODE)
    result = file_display(request)
    assert(isinstance(result, HTTPNotFound))
