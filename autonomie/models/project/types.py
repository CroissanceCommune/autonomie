# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Project Type management
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)


class ProjectType(DBBASE):
    __tablename__ = "project_type"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    label = Column(
        String(255),
        info={
            "colanderalchemy": {
                "title": u"Libellé",
                "description": u"Libellé présenté aux entrepreneurs",
            }
        },
        nullable=False,
    )
    private = Column(
        Boolean(),
        info={
            "colanderalchemy": {
                "title": u"Nécessite des droits particulires ?",
                "description": u"Les utilisateurs doivent-ils disposer de "
                u"droits particuliers pour accéder à ce type de projet ?"
            }
        }
    )
    editable = Column(Boolean(), default=True)
    active = Column(Boolean(), default=True)

    @classmethod
    def get_by_name(cls, name):
        return cls.query().filter_by(name=name).first()
