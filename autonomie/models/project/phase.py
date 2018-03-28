# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)

from autonomie import forms
from autonomie_base.models.types import (
    PersistentACLMixin,
)
from autonomie_base.models.base import (
    default_table_args,
    DBBASE,
)


class Phase(DBBASE, PersistentACLMixin):
    """
        Phase d'un projet
    """
    __tablename__ = 'phase'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': forms.EXCLUDED},
    )

    project_id = Column(
        ForeignKey('project.id'),
        info={'colanderalchemy': forms.EXCLUDED},
    )

    name = Column("name", String(150), default=u'Phase par défaut')

    project = relationship(
        "Project",
        backref=backref(
            "phases",
            cascade="all, delete-orphan",
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True}
            },
        ),
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True}
        },
    )

    def is_default(self):
        """
            return True if this phase is a default one
        """
        return self.name in (u'Phase par défaut', u"default", u"défaut",)

    @property
    def estimations(self):
        return self.get_tasks_by_type('estimation')

    @property
    def invoices(self):
        return self.get_tasks_by_type('invoice')

    @property
    def cancelinvoices(self):
        return self.get_tasks_by_type('cancelinvoice')

    def get_tasks_by_type(self, type_):
        """
            return the tasks of the passed type
        """
        return [doc for doc in self.tasks if doc.type_ == type_]

    def todict(self):
        """
            return a dict version of this object
        """
        return dict(id=self.id,
                    name=self.name)
