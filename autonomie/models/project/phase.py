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
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)

from autonomie_base.models.types import (
    PersistentACLMixin,
)
from autonomie_base.models.base import (
    default_table_args,
    DBBASE,
)


class SubProject(DBBASE, PersistentACLMixin):
    __tablename__ = "sub_project"
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}},
    )

    name = Column("name", String(150), default=u'Phase par défaut')

    closed = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Ce sous-projet est-il fermé ?"
            }
        },
    )

    subproject_type_id = Column(
        ForeignKey('sub_project_type.id'),
        info={'colanderalchemy': {'title': u'Type de sous-projet'}}
    )
    project_id = Column(
        ForeignKey('project.id'),
        info={'colanderalchemy': {'exclude': True}},
    )

    subproject_type = relationship(
        "SubProjectType",
        info={'colanderalchemy': {'exclude': True}},
    )
    project = relationship(
        "Project",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
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
        info={'colanderalchemy': {'exclude': True}},
    )

    project_id = Column(
        ForeignKey('project.id'),
        info={'colanderalchemy': {'exclude': True}},
    )

    name = Column("name", String(150), default=u'Phase par défaut')

    project = relationship(
        "Project",
        backref=backref(
            "phases",
            cascade="all, delete-orphan",
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True}
            },
        ),
        info={
            'colanderalchemy': {'exclude': True},
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
