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
    File model
"""
import hashlib
from datetime import datetime
from sqlalchemy import (
    Integer,
    Column,
    ForeignKey,
    DateTime,
    String,
)

from sqlalchemy.orm import (
    deferred,
    relationship,
    backref,
)

from sqlalchemy.dialects.mysql.base import LONGBLOB

from autonomie.models.base import (
    default_table_args,
    DBBASE,
    DBSESSION,
)
from autonomie.models.node import Node


class File(Node):
    """
        A file model
    """
    __tablename__ = 'file'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'file'}
    id = Column(Integer, ForeignKey('node.id'), primary_key=True)
    description = Column(String(100), default="")
    data = deferred(Column(LONGBLOB()))
    mimetype = Column(String(100))
    size = Column(Integer)

    def getvalue(self):
        """
        Method making our file object compatible with the common file rendering
        utility
        """
        return self.data

    @property
    def label(self):
        """
        Simple shortcut for getting a label for this file
        """
        return self.description or self.name


class MailHistory(DBBASE):
    """
    Stores the history of mail sent by our application to any company
    """
    __tablename__ = 'mail_history'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    send_at = Column(
        DateTime(),
        default=datetime.now(),
    )

    filename = Column(String(100))
    md5sum = Column(String(100))
    company_id = Column(ForeignKey('company.id'), nullable=True)
    company = relationship(
        "Company",
        backref=backref('mail_history'),
    )


def store_sent_mail(filename, filedatas, company):
    """
    Stores a sent email in the history

    :param filename: The name of the file to send
    :param filedatas: The file datas
    :param obj company: a company instance
    """
    mail_history = MailHistory(
        filename=filename,
        md5sum=hashlib.md5(filedatas).hexdigest(),
        company_id=company.id
    )
    DBSESSION().add(mail_history)
    return mail_history


def check_if_mail_sent(filedatas, company):
    """
    Check if the given file has already been sent
    """
    query = MailHistory.query()
    query = query.filter(MailHistory.company_id==company.id)
    md5sum = hashlib.md5(filedatas).hexdigest()
    query = query.filter(MailHistory.md5sum==md5sum)
    return query.first() is not None
