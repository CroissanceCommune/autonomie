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


class Business(DBBASE, PersistentACLMixin):
    __tablename__ = "business"
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}},
    )

    name = Column(
        String(150),
        info={
            "colanderalchemy": {
                "title": u"Nom du sous-projet",
            }
        }
    )

    closed = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Ce sous-projet est-il fermé ?"
            }
        },
    )

    business_type_id = Column(
        ForeignKey('business_type.id'),
        info={'colanderalchemy': {'title': u"Type d'affaires"}}
    )
    project_id = Column(
        ForeignKey('project.id'),
        info={'colanderalchemy': {'exclude': True}},
    )

    business_type = relationship(
        "BusinessType",
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

    def __json__(self, request):
        """
            return a dict version of this object
        """
        return dict(id=self.id,
                    name=self.name)

    def label(self):
        """
        Return a label representing this phase
        """
        if self.is_default():
            return u"Dossier par défaut"
        else:
            return self.name
