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
import unittest
import locale
from autonomie.views import render_api

class TestIt(unittest.TestCase):
    def test_format_amount(self):
        a = 1525
        b = 1525.3
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        self.assertEqual(render_api.format_amount(a), "15,25")
        self.assertEqual(render_api.format_amount(a, trim=False), "15,25")

        self.assertEqual(render_api.format_amount(b), "15,25")
        self.assertEqual(render_api.format_amount(b, trim=False), "15,25")

        c = 210000
        self.assertEqual(
            render_api.format_amount(c, grouping=False),
            "2100,00"
        )
        self.assertEqual(
            render_api.format_amount(c, grouping=True),
            "2&nbsp;100,00"
        )

        c = 21000000
        self.assertEqual(
            render_api.format_amount(c, trim=False, precision=5),
            "210,00"
        )
        c = 21000004
        self.assertEqual(
            render_api.format_amount(c, trim=False,precision=5),
            "210,00004"
        )
        self.assertEqual(
            render_api.format_amount(c, trim=True, precision=5),
            "210,00"
        )

    def test_format_name(self):
        self.assertEqual(render_api.format_name(None, u"LastName"),
                                                         u"LASTNAME ")
        self.assertEqual(render_api.format_name(u"Firstname", None),
                                                        u" Firstname")

    def test_remove_tag(self):
        self.assertEqual(
            render_api.remove_tag("<test><br />", "<br />"),
            "<test>",
        )

    def test_clean_linebreaks(self):
        self.assertEqual(
            render_api.clean_linebreaks("""
                             <p>TEst</p>
                             <p>    </p>
                             <br /> <div></div>
                             """),
            """<p>TEst</p>"""
        )
