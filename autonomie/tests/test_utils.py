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

from mock import Mock

from autonomie.forms import (
    merge_session_with_post,
    flatten_appstruct,
)
from autonomie.utils.files import (
    encode_path,
    decode_path,
    issubdir,
    filesizeformat,
)
from autonomie.utils.rest import (
    RestJsonRepr,
    RestError,
)
from autonomie.utils.ascii import (
    force_ascii,
)
from autonomie.utils import date


def test_merge_session_with_post():
    session = Mock()
    post = dict(id=12, name="Dupont", lastname="Jean",
                            accounts=['admin', 'user'])
    merge_session_with_post(session, post)
    assert session.name == 'Dupont'
    assert "admin" in session.accounts

def test_flatten_appstruct():
    appstruct = {'key1':'value1', 'key2': {'key3': 'value3'}}
    assert flatten_appstruct(appstruct) == {'key1': 'value1', 'key3': 'value3'}


def test_avatar(dbsession, config, get_csrf_request):
    from autonomie.utils.avatar import get_avatar
    config.testing_securitypolicy(userid="user1_login")
    request = get_csrf_request()
    request.dbsession = dbsession
    avatar = get_avatar(request)
    assert avatar.lastname == "user1_lastname"


def test_load_value(dbsession):
    from autonomie.models.config import get_config, Config
    dbsession.add(Config(name="name", value="value"))
    dbsession.flush()
    all_ = get_config()
    assert "name" in all_.keys()
    assert all_["name"] == "value"


def test_encode_decode():
    st = u"$deù % ù$ùdeù % - /// //  \ \dekodok %spkoij  idje  ' kopk \""
    encoded = encode_path(st)
    assert decode_path(encoded) == st

def test_issubdir():
    assert(issubdir("/root/foo", "/root/foo/bar"))
    assert(not issubdir("/root/foo", "/root/bar"))
    assert(not issubdir("/root/foo", "/root/../../foo/bar"))

def test_filesizeformat():
    assert(filesizeformat(1024, 0) == "1ko")
    assert(filesizeformat(1024, 1) == "1.0ko")
    assert(filesizeformat(1024*1024, 0) == "1Mo")
    assert(filesizeformat(1024*1024, 1) == "1.0Mo")


def test_force_ascii():
    assert force_ascii("éco") == u"eco"
    assert force_ascii(5) == "5"
    assert force_ascii(u"éco") == "eco"


class DummyModel(dict):
    def appstruct(self):
        return self


class DummySchema:
    def serialize(self, datadict):
        return {'schemakey':datadict['schemakey']*2}

    def bind(self, **params):
        self.bind_params = params
        return self


class DummyJsonRepr(RestJsonRepr):
    schema = DummySchema()


def test_json():
    datas = DummyModel(schemakey=10, otherkey="dummy")
    jsonrepr = DummyJsonRepr(datas)
    assert(set(jsonrepr.__json__('request').keys())\
            .difference(datas.keys()) == set([]))

def test_bind_params():
    jsonrepr = DummyJsonRepr({}, bind_params=dict(test=5))
    schema = jsonrepr.get_schema("request")
    assert(schema.bind_params.keys() == ['test'])
    jsonrepr = DummyJsonRepr({})
    schema = jsonrepr.get_schema("request")
    assert(schema.bind_params.keys() == ['request'])


def test_it(config):
    err = RestError({}, 151)
    assert(err.status == u"151 Continue")
    assert(err.content_type == 'application/json')


def test_script_utils():
    from autonomie.scripts.utils import get_value
    args = {'--test': 'toto', '--': 'titi'}
    assert get_value(args, 'test', '') == 'toto'
    assert get_value(args, 'test1', 'test') == 'test'

def test_str_to_date():
    import datetime
    assert date.str_to_date("12/11/2014") == datetime.datetime(2014, 11, 12)
    assert date.str_to_date("12-11-2014") == datetime.datetime(2014, 11, 12)
    assert date.str_to_date(None) == ""

