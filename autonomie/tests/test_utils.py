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
from mock import Mock

from autonomie.utils.forms import merge_session_with_post, XHttpForm

from .base import BaseTestCase

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

class TestAvatar(BaseTestCase):
    """
        A dummy user is created in test initiliazition
    """
    def test_avatar(self):
        from autonomie.utils.avatar import get_build_avatar
        build_avatar = get_build_avatar(self.session)
        request = Mock()
        request.session = dict()
        build_avatar("WrongUser", request)
        self.assertTrue(request.session['user'] is None)
        request = Mock()
        request.session = dict()
        build_avatar("user1_login", request)
        self.assertTrue(request.session['user'].email == "user1@test.fr")

class TestConfig(BaseTestCase):
    def test_load_value(self):
        from autonomie.utils.config import load_config
        all_ = load_config(self.session)
        self.assertTrue("hostname" in all_.keys()
                        and "coop_interviewergroup" in all_.keys())
        one_ = load_config(self.session, "hostname")
        self.assertEqual(one_['hostname'], "autonomie.localhost")
