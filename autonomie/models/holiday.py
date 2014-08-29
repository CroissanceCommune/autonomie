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
    Holiday model used to store employee's holiday declaration
"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from autonomie.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.forms import EXCLUDED

class Holiday(DBBASE):
    """
        Holidays table
        Stores the start and end date for holiday declaration
        user_id
        start_date
        end_date
    """
    __tablename__ = "holiday"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey('accounts.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    user = relationship(
        "User",
        backref=backref(
            "holidays",
            info={'colanderalchemy': EXCLUDED},
            order_by="Holiday.start_date",
        ),
        primaryjoin="Holiday.user_id==User.id"
    )

    def __json__(self, request):
        return dict(
                id=self.id,
                user_id=self.user_id,
                start_date=self.start_date,
                end_date=self.end_date)
