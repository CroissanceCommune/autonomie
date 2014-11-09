# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
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


from autonomie.panels.company import (
        _get_page_number,
        _make_get_list_url,
        _get_post_int,
        _get_items_per_page,
        )

def test__get_page_number(get_csrf_request):
    request = get_csrf_request(post={'page_nb':"5"})
    assert _get_page_number(request, 'page_nb') == 5
    assert _get_page_number(request, 'nutts') == 0

def test__make_get_list_url():
    func = _make_get_list_url("mylist")
    assert func(0) == "#mylist/0"
    assert func(5) == "#mylist/5"

def test__get_post_int(get_csrf_request):
    request = get_csrf_request(post={'posted_int': '5'})
    assert _get_post_int(request, 'posted_int', 2) == 5
    assert _get_post_int(request, 'nutts', 2) == 2

def test__get_items_per_page(get_csrf_request):
    default = 5

    request = get_csrf_request()
    assert _get_items_per_page(request, 'item_pp') == default
    request = get_csrf_request(cookies={'item_pp':'abc'})
    assert _get_items_per_page(request, 'item_pp') == default
    request = get_csrf_request(post={'item_pp': 'abc'})
    assert _get_items_per_page(request, 'item_pp') == default

    request = get_csrf_request(post={'item_pp': 5})
    assert _get_items_per_page(request, 'item_pp') == 5

    request = get_csrf_request(
            post={'item_pp': '5'},
            cookies={'item_pp':'10'}
            )
    assert _get_items_per_page(request, 'item_pp') == 5

    request = get_csrf_request(cookies={'item_pp':'10'})
    assert _get_items_per_page(request, 'item_pp') == 10

    request = get_csrf_request(post={'item_pp': 'abc'},
            cookies={'item_pp':'10'})
    assert _get_items_per_page(request, 'item_pp') == 10
