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
from autonomie.utils.math_utils import floor
from autonomie.utils.math_utils import amount

from .base import BaseTestCase
from .base import BaseViewTest

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

class TestMathUtils(BaseTestCase):
    def test_floor(self):
        # Ref #727
        a = 292.65 * 100.0
        self.assertEqual(floor(a), 29265)
        a = 29264.91
        self.assertEqual(floor(a), 29264)

    def test_amount(self):
        # Ref #727
        a = 192.65
        self.assertEqual(amount(a), 19265)
        a = 192.6555
        self.assertEqual(amount(a), 19265)
        self.assertEqual(amount(a, 4), 1926555)
