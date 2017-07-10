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
    Custom colander types
"""
import colander
from autonomie.compute.math_utils import (
    amount,
    integer_to_amount,
)


def specialfloat(self, value):
    """
        preformat the value before passing it to the float function
    """
    if isinstance(value, unicode):
        value = value.replace(u'€', '').replace(u',', '.').replace(u' ', '')
    return float(value)


class QuantityType(colander.Number):
    """
        Preformat unicode supposed to be numeric entries
    """
    num = specialfloat


class _AmountType(colander.Number):
    """
        preformat an amount before considering it as a float object
        then *100 to store it into database
    """
    num = specialfloat

    def __init__(self, precision=2):
        colander.Number.__init__(self)
        self.precision = precision

    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null

        try:
            return str(integer_to_amount(self.num(appstruct), self.precision))
        except Exception:
            raise colander.Invalid(
                node,
                u"\"{val}\" n'est pas un montant valide".format(val=appstruct),
            )

    def deserialize(self, node, cstruct):
        if cstruct != 0 and not cstruct:
            return colander.null

        try:
            return amount(self.num(cstruct), self.precision)
        except Exception:
            raise colander.Invalid(
                node,
                u"\"{val}\" n'est pas un montant valide".format(val=cstruct)
            )


class Integer(colander.Number):
    """
        Fix https://github.com/Pylons/colander/pull/35
    """
    num = int

    def serialize(self, node, appstruct):
        if appstruct in (colander.null, None):
            return colander.null
        try:
            return str(self.num(appstruct))
        except Exception:
            raise colander.Invalid(
                node,
                u"'${val}' n'est pas un nombre".format(val=appstruct)
            )


class AmountType(colander.deferred):

    def __init__(self, precision=2):

        def deferred_amount_type(node, kw):
            translate = kw.get('translate', True)
            if translate:
                return _AmountType(precision)
            else:
                return Integer()

        colander.deferred.__init__(self, deferred_amount_type)

    def __call__(self, node=None, kw=None):
        if node is None:  # Colanderalchemy bug #102
            return self
        else:
            return colander.deferred.__call__(self, node, kw)
