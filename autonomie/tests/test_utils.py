# -*- coding: utf-8 -*-
# * File Name : test_utils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 26-03-2012
# * Last Modified :
#
# * Project : autonomie
#
import colander
from pyramid import testing
from mock import Mock

from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.files import (encode_path, decode_path, issubdir,
        filesizeformat)

from autonomie.utils.rest import RestJsonRepr, RestError

from .base import BaseTestCase
from .base import BaseViewTest
from autonomie.tests.base import BaseFunctionnalTest

class DummySchema(colander.MappingSchema):
    lastname = colander.SchemaNode(colander.String(), title='Nom')

class TestFormUtils(BaseTestCase):
    def test_merge_session_with_post(self):
        session = Mock()
        post = dict(id=12, name="Dupont", lastname="Jean",
                                accounts=['admin', 'user'])
        merge_session_with_post(session, post)
        self.assertTrue(session.name == 'Dupont')
        self.assertTrue("admin" in session.accounts)


class TestAvatar(BaseViewTest):
    """
        A dummy user is created in test initiliazition
    """
    def test_avatar(self):
        from autonomie.utils.avatar import get_avatar
        self.config.testing_securitypolicy(userid="authenticated")
        request = testing.DummyRequest()
        request._user = Mock(name="username")
        avatar = get_avatar(request, self.session)
        self.assertEqual(avatar, request._user)
        self.config.testing_securitypolicy(userid="contractor1")
        request = testing.DummyRequest()
        avatar = get_avatar(request, self.session)
        self.assertEqual(avatar.lastname, "LASTNAME_contractor1")


class TestConfig(BaseTestCase):
    def test_load_value(self):
        from autonomie.models.config import get_config, Config
        self.session.add(Config(app="test", name="name", value="value"))
        self.session.flush()
        all_ = get_config()
        self.assertTrue("name" in all_.keys() and all_["name"] == "value")


class TestFileSystem(BaseTestCase):
    def test_encode_decode(self):
        st = u"$deù % ù$ùdeù % - /// //  \ \dekodok %spkoij  idje  ' kopk \""
        encoded = encode_path(st)
        self.assertEqual(decode_path(encoded), st)

    def test_issubdir(self):
        self.assertTrue(issubdir("/root/foo", "/root/foo/bar"))
        self.assertFalse(issubdir("/root/foo", "/root/bar"))
        self.assertFalse(issubdir("/root/foo", "/root/../../foo/bar"))

    def test_filesizeformat(self):
        self.assertEqual(filesizeformat(1024, 0), "1ko")
        self.assertEqual(filesizeformat(1024, 1), "1.0ko")
        self.assertEqual(filesizeformat(1024*1024, 0), "1Mo")
        self.assertEqual(filesizeformat(1024*1024, 1), "1.0Mo")


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


class TestRestJsonRepr(BaseTestCase):
    def test_json(self):
        datas = DummyModel(schemakey=10, otherkey="dummy")
        jsonrepr = DummyJsonRepr(datas)
        self.assertEqual(set(jsonrepr.__json__('request').keys())\
                .difference(datas.keys()), set([]))

    def test_bind_params(self):
        jsonrepr = DummyJsonRepr({}, bind_params=dict(test=5))
        schema = jsonrepr.get_schema("request")
        self.assertEqual(schema.bind_params.keys(), ['test'])
        jsonrepr = DummyJsonRepr({})
        schema = jsonrepr.get_schema("request")
        self.assertEqual(schema.bind_params.keys(), ['request'])


class TestRestError(BaseFunctionnalTest):
    def test_it(self):
        err = RestError({}, 151)
        self.assertEqual(err.status, u"151 Continue")
        self.assertEqual(err.content_type, 'application/json')
