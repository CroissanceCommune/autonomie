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
    Autonomie specific exception
"""


class BadRequest(Exception):
    """
    Exception raised when the request is invalid (form invalid datas ...)
    """
    message = u"La requête est incorrecte"

    def messages(self):
        """
        Used to fit colander's Invalid exception api
        """
        return [self.message]

    def asdict(self):
        return {'erreur': self.message}


class Forbidden(Exception):
    """
        Forbidden exception, used to raise a forbidden action error
    """
    message = u"Vous n'êtes pas autorisé à effectuer cette action"


class SignatureError(Forbidden):
    """
        Exception for status modification calls with the wrong signature
    """
    message = u"Des informations manquent pour effectuer cette action"
