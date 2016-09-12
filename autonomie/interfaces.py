# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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

from zope.interface import Interface


class ITreasuryInvoiceProducer(Interface):
    """
    Interface for the class that will produce treasury invoice export lines
    """
    def get_book_entries(self, invoicelist):
        pass


class ITreasuryInvoiceWriter(Interface):
    """
    Interface for the module handling the generation of the tabular export file
    """
    def set_datas(self, lines):
        """
        Set the tabular datas that will be written in the output file
        """
        pass
