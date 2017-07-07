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
"""
Customer query service
"""
from autonomie_base.models.base import DBSESSION
from autonomie.utils.formatters import format_civilite


class CustomerService(object):
    @classmethod
    def get_tasks(cls, instance, type_str=None):
        from autonomie.models.task import Task
        query = DBSESSION().query(Task)
        query = query.filter_by(customer_id=instance.id)

        if type_str is not None:
            query = query.filter(Task.type_ == type_str)
        else:
            query = query.filter(
                Task.type_.in_(('invoice', 'cancelinvoice', 'estimation'))
            )
        return query

    @classmethod
    def count_tasks(cls, instance):
        return cls.get_tasks(instance).count()

    @classmethod
    def format_name(cls, instance):
        """
        Format the name of a customer regarding the available datas
        :param obj customer: A Customer instance
        :rtype: str
        """
        res = u""
        if instance.civilite:
            res += u"{0} ".format(format_civilite(instance.civilite))
            res += instance.lastname
            if instance.firstname:
                res += u" {0}".format(instance.firstname)
        return res

    @classmethod
    def get_label(cls, instance):
        """
        Return the label suitable for the given instance
        :param obj instance: A Customer instance
        :returns: The label
        :rtype: str
        """
        if instance.type_ == 'company':
            return instance.name
        else:
            return cls.format_name(instance)

    @classmethod
    def get_address(cls, instance):
        """
        Return the address suitable for the given instance
        :param obj instance: A Customer instance
        :returns: The address
        :rtype: str
        """
        address = u""
        if instance.type_ == 'company':
            address += u"{0}\n".format(instance.name)
        name = cls.format_name(instance)
        if name:
            address += u"{0}\n".format(name)

        address += u"{0}\n".format(instance.address)
        address += u"{0} {1}".format(instance.zip_code, instance.city)

        country = instance.country
        if country is not None and country.lower() != "france":
            address += u"\n{0}".format(country)
        return address
