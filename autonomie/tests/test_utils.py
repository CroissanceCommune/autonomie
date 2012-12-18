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
from deform.form import Form
from pyramid import testing
from mock import Mock

from autonomie.utils.forms import merge_session_with_post, XHttpForm

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

    def test_xhttpform(self):
        schema = DummySchema()
        f = XHttpForm(schema)
        f.add_message("Jean is wrong")
        f.add_message("Jean is right")
        html = f.render()
        self.assertTrue("Jean is wrong" in html)
        self.assertTrue('Jean is right' in html)
        f.reset_messages()
        self.assertTrue("Jean is wrong" not in f.render())

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
