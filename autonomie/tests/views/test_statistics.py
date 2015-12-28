# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:#       * Arezki Feth <f.a@majerti.fr>;
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

import pytest
from autonomie.models import statistics as models

@pytest.fixture
def sheet(dbsession):
    sheet = models.StatisticSheet(title=u"test_sheet")
    dbsession.add(sheet)
    dbsession.flush()
    return sheet

@pytest.fixture
def full_sheet(dbsession, sheet):
    entry = models.StatisticEntry(
        title=u"test_entry",
        description=u"test entry",
        sheet_id=sheet.id,
    )
    dbsession.add(entry)
    dbsession.flush()
    criterion_1 = models.CommonStatisticCriterion(
        key="parcours_num_hours",
        method="true",
        entry_id=entry.id
    )
    criterion_2 = models.OrStatisticCriterion(
        entry_id=entry.id,
    )
    dbsession.add(criterion_1)
    dbsession.add(criterion_2)
    dbsession.flush()

    criterion_21 = models.CommonStatisticCriterion(
        key=u"coordonnees_firstname",
        method="nnll",
        entry_id=entry.id,
        parent_id=criterion_2.id,
    )
    criterion_22 = models.CommonStatisticCriterion(
        key=u"coordonnees_lastname",
        method="sw",
        entry_id=entry.id,
        parent_id=criterion_2.id,
    )
    dbsession.add(criterion_21)
    dbsession.add(criterion_22)
    dbsession.flush()
    return sheet


def test_rest_sheet(full_sheet, get_csrf_request_with_db):
    from autonomie.views.statistics import RestStatisticSheet
    request = get_csrf_request_with_db()
    request.context = full_sheet
    view = RestStatisticSheet(request)
    res = view.get()

    assert res['sheet'].title == 'test_sheet'
    # Le lien entre criterion est secondaire
    assert len(res['entries'][0].criteria) == 4


def test_rest_entry_add(full_sheet, get_csrf_request_with_db):
    from autonomie.views.statistics import RestStatisticEntry
    appstruct = {
        "title": u"Nouvelle entrée",
        "description": u"Description",
    }
    request = get_csrf_request_with_db()
    request.context = full_sheet
    request.json_body = appstruct
    view = RestStatisticEntry(request)
    res = view.post()

    entry = full_sheet.entries[1]
    assert entry.title == u'Nouvelle entrée'
    assert entry.description == u"Description"


def test_rest_entry_edit(full_sheet, get_csrf_request_with_db):
    from autonomie.views.statistics import RestStatisticEntry
    appstruct = {
        "title": u"Entrée éditée",
    }
    request = get_csrf_request_with_db()
    request.context = full_sheet.entries[0]
    request.json_body = appstruct
    view = RestStatisticEntry(request)
    res = view.put()

    entry = full_sheet.entries[0]
    assert entry.title == u'Entrée éditée'
    assert entry.description == u"test entry"

