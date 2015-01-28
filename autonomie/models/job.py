# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Celery tasks related models
"""
from datetime import datetime
from sqlalchemy import (
    Integer,
    Column,
    ForeignKey,
    String,
    DateTime,
    Text,
)
from autonomie.models.types import (
    JsonEncodedList,
    PersistentACLMixin,
)
from autonomie.models.base import (
    DBBASE,
    default_table_args,
)

class Job(DBBASE, PersistentACLMixin):
    """
    Base job model, used to communicate a job's status between the main pyramid
    app and celery asynchronous tasks
    """
    __tablename__ = 'job'
    __table_args__ = default_table_args
    __mapper_args__ = {
        'polymorphic_on': 'type_',
        'polymorphic_identity':'job'
    }
    label = u"Tâche générique"
    id = Column(
        Integer,
        primary_key=True,
    )
    jobid = Column(
        String(255),
        nullable=True,
    )
    status = Column(
        String(20),
        default='planned',
    )
    created_at = Column(
        DateTime(),
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime(),
        default=datetime.now(),
        onupdate=datetime.now()
    )
    type_ = Column(
        'type_',
        String(30),
        nullable=False,
    )

    def todict(self):
        return dict(
            label=self.label,
            jobid=self.jobid,
            status=self.status,
            created_at=self.created_at.strftime("%d/%m/%Y à %H:%M"),
            updated_at=self.updated_at.strftime("%d/%m/%Y à %H:%M"),
        )


class CsvImportJob(Job):
    """
    Store csv importation job status
    """
    __tablename__ = 'csv_import_job'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'csv_import'}
    id = Column(Integer, ForeignKey('job.id'), primary_key=True)
    messages = Column(JsonEncodedList, default=None)
    error_messages = Column(JsonEncodedList, default=None)
    in_error_csv = Column(Text(), default=None)
    unhandled_datas_csv = Column(Text(), default=None)
    label = u"Import de données"

    def is_not_void_str(self, value):
        """
        Return True if the string contains datas
        """
        return not (value is None or len(value) == 0)


    def todict(self):
        res = Job.todict(self)
        res['label'] = self.label
        res['messages'] = self.messages
        res['error_messages'] = self.error_messages
        res['has_errors'] = self.is_not_void_str(self.in_error_csv)
        res['has_unhandled_datas'] = self.is_not_void_str(
            self.unhandled_datas_csv
        )
        return res


class MailingJob(Job):
    """
    Store mailing job status
    """
    __tablename__ = 'mailing_job'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'mailing'}
    id = Column(Integer, ForeignKey('job.id'), primary_key=True)
    messages = Column(JsonEncodedList, default=None)
    error_messages = Column(JsonEncodedList, default=None)
    label = u"Envoi de mail"

    def todict(self):
        res = Job.todict(self)
        res['label'] = self.label
        res['messages'] = self.messages
        res['error_messages'] = self.error_messages
        return res
