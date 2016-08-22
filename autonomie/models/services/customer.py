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
from autonomie.models.base import DBSESSION


class CustomerService(object):
    @classmethod
    def get_tasks(cls, instance, type_str):
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
