# -*- coding: utf-8 -*-
# * File Name : test_treasury_files.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 12-02-2013
# * Last Modified :
#
"""
    test treasury files views
"""
import os
from mock import Mock
from autonomie.tests.base import DATASDIR, BaseViewTest
from autonomie.views.treasury_files import (Treasury,
        isprefixed, code_is_not_null)

CODE = "125"


#def make_directories():
#    for directory in ('tresorerie', 'resultat', 'salaire'):
#        for year in range(2010,2012):
#            for month in range(1, 13):
#                path = os.path.join(DATASDIR, directory, str(year), str(month))
#                os.system("mkdir -p %s" % path)
#                for i in range(4):
#                    fname = "%s_%s_test.pdf" % (CODE, i)
#                    fpath = os.path.join(path, fname)
#                    os.system("touch %s" % fpath)


class TestDirectory(BaseViewTest):
    def setUp(self):
        super(TestDirectory, self).setUp()
        #make_directories()

    def get_request(self):
        request = self.get_csrf_request()
        request.registry.settings["autonomie.ftpdir"] = DATASDIR
        return request

    def test_digit_subdirs(self):
        path = os.path.join(DATASDIR, "tresorerie", "2010")
        request = self.get_request()
        view = Treasury(request)
        dirs = list(view.digit_subdirs(path))
        self.assertEqual(len(dirs), 12)

    def test_list_files(self):
        path = os.path.join(DATASDIR, "tresorerie", "2010", "1")
        request = self.get_csrf_request()
        view = Treasury(request)
        self.assertEqual(len(view.list_files(path, prefix='')), 0)
        self.assertEqual(len(view.list_files(path, prefix='12')), 0)
        self.assertEqual(len(view.list_files(path, prefix='1256')), 0)
        self.assertEqual(len(view.list_files(path, prefix='125')), 4)

    def test_list_files_sorted(self):
        request = self.get_csrf_request()
        path = os.path.join(DATASDIR, "tresorerie", "2010", "1")
        view = Treasury(request)
        files = view.list_files(path, prefix='125')
        prev = files[0]
        for f_ in files[1:]:
            self.assertTrue(cmp(f_.name, prev.name), 1)
            prev = f_

    def test_isprefixed(self):
        self.assertTrue(isprefixed("256_bar.pdf", "256"))
        self.assertTrue(isprefixed("256_bar.pdf"))
        self.assertFalse(isprefixed("256_bar.pdf", "32"))
        self.assertFalse(isprefixed("256_bar.pdf", "2567"))
        self.assertFalse(isprefixed("256_bar.pdf", "25"))

    def test_code_is_not_null(self):
        self.assertTrue(code_is_not_null("2"))
        for i in '0', '', None:
            self.assertFalse(code_is_not_null(i))
