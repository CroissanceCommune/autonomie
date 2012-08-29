# -*- coding: utf-8 -*-
# * File Name : custom_types.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-06-2012
# * Last Modified :
#
# * Project :Autonomie
#
"""
    Custom colander types
"""
import colander

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

class AmountType(colander.Number):
    """
        preformat an amount before considering it as a float object
        then *100 to store it into database
    """
    num = specialfloat
    def serialize(self, node, appstruct):
        if appstruct is colander.null:
            return colander.null

        try:
            return str(self.num(appstruct) / 100.0)
        except Exception:
            raise colander.Invalid(node,
                          u"\"{val}\" n'est pas un montant valide".format(
                                val=appstruct),
                          )
    def deserialize(self, node, cstruct):
        if cstruct != 0 and not cstruct:
            return colander.null

        try:
            return int(self.num(cstruct) * 100.0)
        except Exception:
            raise colander.Invalid(node,
                          u"\"{val}\" n'est pas un montant valide".format(
                            val=cstruct)
                          )

