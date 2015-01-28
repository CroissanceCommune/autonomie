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
import pytest
from mock import Mock
from pyramid.exceptions import HTTPForbidden, HTTPNotFound
from autonomie.views.treasury_files import (
    TreasuryFilesView,
    IncomeStatementFilesView,
    SalarySheetFilesView,
    isprefixed,
    get_code_compta,
    code_is_not_null,
    digit_subdirs,
    file_display,
    list_files,
    AdminTreasuryView,
    MailTreasuryFilesView,
    get_root_directory,
)

CODE = "125"


@pytest.fixture
def company_125(dbsession):
    from autonomie.models.company import Company
    c = Company(name=u'testit', code_compta=CODE, email="a@a.fr")
    dbsession.add(c)
    return c


def test_digit_subdirs(settings):
    path = os.path.join(settings['autonomie.ftpdir'], "tresorerie", "2010")
    dirs = list(digit_subdirs(path))
    assert len(dirs) == 12


def test_list_files(settings):
    path = os.path.join(settings['autonomie.ftpdir'], "tresorerie", "2010", "1")
    assert len(list_files(path, prefix='')) == 12
    assert len(list_files(path, prefix='12')) == 0
    assert len(list_files(path, prefix=CODE+'6')) == 0
    assert len(list_files(path, prefix=CODE)) == 4


def test_list_files_sorted(settings):
    path = os.path.join(settings['autonomie.ftpdir'], "tresorerie", "2010", "1")
    files = list_files(path, prefix=CODE)
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


def test_get_code_compta():
    with pytest.raises(Exception):
        get_code_compta('0')



def test_code_is_not_null():
    assert(code_is_not_null("2"))
    for i in '0', '', None:
        assert(not code_is_not_null(i))


def test_view(config, get_csrf_request):
    request = get_csrf_request()
    request.context = Mock(code_compta=CODE)
    config.add_route('treasury_files', '/')
    for factory in IncomeStatementFilesView, SalarySheetFilesView, TreasuryFilesView:
        view = factory(request)
        result = view.__call__()
        assert len(result['documents'].keys()) == 2
        assert len(result['documents']['2010']) == 12


def test_nutt(config, get_csrf_request):
    request = get_csrf_request()
    request.context = Mock(code_compta="")
    config.add_route('treasury_files', '/')
    for factory in IncomeStatementFilesView, SalarySheetFilesView, TreasuryFilesView:
        view = factory(request)
        assert view()['documents'] == {}


def test_file_view(get_csrf_request):
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

def test_admin_treasury(config, pyramid_request):
    config.add_route("admin_treasury_files", "/{filetype}/{year}/{month}/",)
    view = AdminTreasuryView(None, pyramid_request)
    result_dict = view()
    assert set(result_dict['datas'].keys()) == set(('2010', '2011'))
    assert result_dict['datas']['2011']['9']['nbfiles'] == 12


def test_mail_treasury_files(dbsession, config, get_csrf_request, company_125):
    request = get_csrf_request()
    request.matchdict = {'filetype': 'salaire',
                                 'year': '2010', 'month': '1'}
    view = MailTreasuryFilesView(None, request)
    result_dict = view()
    datas = result_dict['datas']
    assert len(datas.keys()) == 1
    for file_ in datas.values()[0]:
        assert file_['file'].code == file_['company'].code_compta


    form_datas = {
        'force': False,
        'mails': [
            {'company_id': company_125.id, 'attachment': '125_1_test.pdf'},
            {'company_id': company_125.id, 'attachment': '125_2_test.pdf'},
        ],
        'mail_subject': u"Sujet",
        "mail_message": u"Message {company.email} {year} {month}",
    }

    mails = view._prepare_mails(datas, form_datas, get_root_directory(request), '2010', '1')
    assert len(mails) == 2
    assert mails[0]['message'] == u"Message a@a.fr 2010 1"
    assert mails[0]['email'] == 'a@a.fr'

    sent_file = datas[company_125.id][0]['file']
    from autonomie.models.files import store_sent_mail
    history = store_sent_mail(sent_file.path, sent_file.datas, company_125.id)
    dbsession.add(history)

    # Not force and already in history
    form_datas = {
        'force': False,
        'mails': [
            {'company_id': company_125.id, 'attachment': '125_0_test.pdf'},
            {'company_id': company_125.id, 'attachment': '125_1_test.pdf'},
            {'company_id': company_125.id, 'attachment': '125_2_test.pdf'},
            {'company_id': company_125.id, 'attachment': '125_3_test.pdf'},
        ],
        'mail_subject': u"Sujet",
        "mail_message": u"Message {company.email} {year} {month}",
    }

    mails = view._prepare_mails(
        datas, form_datas, get_root_directory(request), '2010', '1')
    assert len(mails) == 3

    # Force and already in history
    form_datas = {
        'force': True,
        'mails': [
            {'company_id': company_125.id, 'attachment': '125_0_test.pdf'},
            {'company_id': company_125.id, 'attachment': '125_1_test.pdf'},
            {'company_id': company_125.id, 'attachment': '125_2_test.pdf'},
            {'company_id': company_125.id, 'attachment': '125_3_test.pdf'},
        ],
        'mail_subject': u"Sujet",
        "mail_message": u"Message {company.email} {year} {month}",
    }

    mails = view._prepare_mails(
        datas, form_datas, get_root_directory(request), '2010', '1')
    assert len(mails) == 4

    # Invalid submitted datas
    form_datas = {
        'force': True,
        'mails': [
            {'company_id': -15, 'attachment': '125_3_test.pdf'},
        ],
        'mail_subject': u"Sujet",
        "mail_message": u"Message {company.email} {year} {month}",
    }

    with pytest.raises(Exception):
        mails = view._prepare_mails(
            datas, form_datas, get_root_directory(request), '2010', '1')
