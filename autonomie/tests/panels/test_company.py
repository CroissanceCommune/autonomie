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


def test_get_page_number(get_csrf_request):
    from autonomie.panels.company_index.utils import get_page_number
    request = get_csrf_request(post={'page_nb':"5"})
    assert get_page_number(request, 'page_nb') == 5
    assert get_page_number(request, 'nutts') == 0

def test_make_get_list_url():
    from autonomie.panels.company_index.utils import make_get_list_url
    func = make_get_list_url("mylist")
    assert func(0) == "#mylist/0"
    assert func(5) == "#mylist/5"

def test_get_post_int(get_csrf_request):
    from autonomie.panels.company_index.utils import get_post_int
    request = get_csrf_request(post={'posted_int': '5'})
    assert get_post_int(request, 'posted_int', 2) == 5
    assert get_post_int(request, 'nutts', 2) == 2

def test_get_items_per_page(get_csrf_request):
    from autonomie.panels.company_index.utils import get_items_per_page
    default = 5

    request = get_csrf_request()
    assert get_items_per_page(request, 'item_pp') == default
    request = get_csrf_request(cookies={'item_pp':'abc'})
    assert get_items_per_page(request, 'item_pp') == default
    request = get_csrf_request(post={'item_pp': 'abc'})
    assert get_items_per_page(request, 'item_pp') == default

    request = get_csrf_request(post={'item_pp': 5})
    assert get_items_per_page(request, 'item_pp') == 5

    request = get_csrf_request(
            post={'item_pp': '5'},
            cookies={'item_pp':'10'}
            )
    assert get_items_per_page(request, 'item_pp') == 5

    request = get_csrf_request(cookies={'item_pp':'10'})
    assert get_items_per_page(request, 'item_pp') == 10

    request = get_csrf_request(post={'item_pp': 'abc'},
            cookies={'item_pp':'10'})
    assert get_items_per_page(request, 'item_pp') == 10
