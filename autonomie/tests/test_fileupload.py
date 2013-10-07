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
    Tests
"""
import os
from mock import MagicMock
from pyramid import testing

from .base import BaseFunctionnalTest
from .base import BaseViewTest
from .base import TMPDIR, DATASDIR
from autonomie.utils import fileupload

FAKEURL = "/assets/company/stuff"

class TestFileTempStore(BaseFunctionnalTest):
    def test_setitem(self):
        request = self.get_csrf_request()
        session = request.session
        tempstore = fileupload.FileTempStore(session, TMPDIR, FAKEURL)
        self.assertEqual(None, tempstore.preview_url("dummy"))
        #coming from database
        cstruct1 = {'uid':'test', 'filename':'testfile1.jpg'}
        tempstore[cstruct1['uid']] = cstruct1
        cstruct1['mimetype'] = None
        cstruct1['size'] = None
        self.assertEqual(tempstore.get(cstruct1['uid']), cstruct1)
        self.assertEqual(tempstore.get(cstruct1['uid'])['preview_url'],
                        os.path.join(FAKEURL, cstruct1['filename']))

        # just submitted
        cstruct2 = {'uid':'test', 'filename':'testfile2.jpg',
                    'fp':file(os.path.join(DATASDIR, 'image.jpg'), 'r'),
                    'mimetype':'image/jpeg', 'size':15}
        tempstore[cstruct2['uid']] = cstruct2
        self.assertEqual(tempstore.get(cstruct2['uid'])['mimetype'],
                                                cstruct2['mimetype'])
        self.assertFalse('fp' in tempstore.get(cstruct2['uid']).keys())
        self.assertTrue(os.path.isfile(os.path.join(TMPDIR, 'testfile2.jpg')))
        self.assertTrue(tempstore.get(cstruct2['uid'])['preview_url'],
                                os.path.join(FAKEURL, cstruct2['filename']))

class TestFileTempStore2(BaseFunctionnalTest):
    def test_get_filepath(self):
        request = self.get_csrf_request()
        session = request.session
        tempstore = fileupload.FileTempStore(session, TMPDIR, FAKEURL)
        self.assertEqual(tempstore.get_filepath("test"),
                        os.path.join(TMPDIR, "test"))


class TestFileTempStore3(BaseFunctionnalTest):
    def test_filter(self):
        request = self.get_csrf_request()
        session = request.session

        def void(file_obj):
            file_obj.write("Nope")
            return file_obj
        filters = [void]

        tempstore = fileupload.FileTempStore(session, TMPDIR, FAKEURL,
                                                        filters=filters)
        testfile = os.path.join(TMPDIR, "testfile")
        with file(testfile, "w") as f_obj:
            f_obj.write("There are some datas")

        cstruct2 = {'uid':'test', 'filename':'testfile3.jpg',
                'fp':file(testfile, 'w+b'),
                'mimetype':'image/jpeg', 'size':15}
        tempstore[cstruct2['uid']] = cstruct2
        # We verify the content has been passed through our filter before being
        # passed to the destination file
        content = file(os.path.join(TMPDIR, "testfile3.jpg"), 'r')
        self.assertEqual(content.read(), "Nope")
