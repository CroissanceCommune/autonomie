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
    __colanderalchemy_config__ = {
        "help_msg": u"""Les types de projets permettent de prédéfinir des
        comportements spécifiques (documents à rattacher, modèles à utiliser
        pour les PDFs, mentions ...)"""
    }
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
        unique=True,
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
    default = Column(
        Boolean(),
        default=False,
        info={
            "colanderalchemy": {
                "title": u"Ce type de projet est-il proposé par défaut ?",
            }
        }
    )

    @classmethod
    def get_by_name(cls, name):
        return cls.query().filter_by(name=name).first()

    def is_used(self):
        """
        Check if there is a project using this specific type
        """
        from autonomie.models.project.project import Project
        return Project.query().filter_by(project_type_id=self.id).count() > 0
