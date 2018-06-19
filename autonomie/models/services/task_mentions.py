# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie_base.models.base import DBSESSION
from autonomie.models.project.types import BusinessType


class TaskMentionService(object):
    @classmethod
    def populate(cls, task):
        with DBSESSION.no_autoflush:
            task.mandatory_mentions = BusinessType.get_mandatory_mentions(
                task.business_type_id,
                task.type_,
            )
