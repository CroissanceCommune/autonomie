"""
    Custom colander types
"""
import colander
from autonomie.compute.math_utils import amount


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
            return amount(self.num(cstruct))
        except Exception:
            raise colander.Invalid(node,
                          u"\"{val}\" n'est pas un montant valide".format(
                            val=cstruct)
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
            raise colander.Invalid(node,
                       u"'${val}' n'est pas un nombre".format(val=appstruct))