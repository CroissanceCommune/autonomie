# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Project Type management
"""
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    not_,
)
from sqlalchemy.orm import (
    relationship,
    load_only,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)


ProjectTypeSubProjectType = Table(
    'project_type_sub_project_type',
    DBBASE.metadata,
    Column("project_type_id", Integer, ForeignKey('project_type.id')),
    Column("sub_project_type_id", Integer, ForeignKey('sub_project_type.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine']
)


class BaseProjectType(DBBASE):
    __tablename__ = 'base_project_type'
    __table_args__ = default_table_args
    __mapper_args__ = {
        'polymorphic_on': 'type_',
        'polymorphic_identity': 'base_project_type',
    }
    id = Column(Integer, primary_key=True)
    type_ = Column(
        'type_',
        String(30),
        info={'colanderalchemy': {'exclude': True}},
        nullable=False,
    )
    private = Column(
        Boolean(),
        info={
            "colanderalchemy": {
                "title": u"Nécessite un rôle particulier ?",
                "description": u"Les utilisateurs doivent-ils disposer d'un "
                u"rôle particulier pour utiliser ce type ?"
            }
        }
    )
    name = Column(
        String(50),
        info={
            'colanderalchemy': {
                "title": u"Nom interne",
                "description": u"Le nom interne est utilisé pour définir les "
                u"rôles des utilisateurs accédant à ce type."
            }
        }
    )
    editable = Column(Boolean(), default=True)
    active = Column(Boolean(), default=True)

    @classmethod
    def unique_label(cls, label, type_id):
        """
        Check if a label is unique

        :param str label: Label to check
        :param int type_id: The type id to exclude
        :rtype: bool
        """
        query = cls.query()
        if type_id:
            query = query.filter(not_(cls.id == type_id))
        count = query.filter(cls.label == label).count()
        return count == 0

    @classmethod
    def query_for_select(cls):
        """
        Query project types for selection purpose
        """
        query = DBSESSION().query(cls).options(
            load_only('id', 'label', 'private')
        )
        query = query.filter_by(active=True)
        return query


class ProjectType(BaseProjectType):
    __tablename__ = "project_type"
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'project_type'}
    __colanderalchemy_config__ = {
        "help_msg": u"""Les types de projets permettent de prédéfinir des
        comportements spécifiques (documents à rattacher, modèles à utiliser
        pour les PDFs, mentions ...)"""
    }
    id = Column(
        ForeignKey('base_project_type.id'),
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}}
    )
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


class SubProjectType(BaseProjectType):
    __tablename__ = "sub_project_type"
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'sub_project_type'}
    __colanderalchemy_config__ = {
        "help_msg": u"""Les types d'affaire permettent de prédéfinir des
        comportements spécifiques.
    Ex: Un type d'affaire 'Formation' permet de regrouper les documents
    liés à la formation.
    Il va ensuite être possible de spécifier :
        - Des mentions à inclure dans les documents placées dans cette affaire
        - Les documents requis à la validation des devis ou des factures
        - Le modèle de document à utiliser pour générer les devis/factures
        - Les modèles de document à proposer pour générer les documents
        spécifiques (livret d'accueil ...)
    """
    }
    id = Column(
        ForeignKey('base_project_type.id'),
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}}
    )
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
    project_type_id = Column(
        ForeignKey('project_type.id'),
        info={
            "colanderalchemy": {
                "title": u"Ce type d'affaire est utilisé par défaut pour "
                u"les projets de type :"
            }
        }
    )

    project_type = relationship(
        "ProjectType",
        primaryjoin="ProjectType.id==SubProjectType.project_type_id",
        info={
            'colanderalchemy': {'exclude': True}
        }
    )

    other_project_types = relationship(
        "ProjectType",
        secondary=ProjectTypeSubProjectType,
        info={
            'colanderalchemy': {
                'title': u"Ce type d'affaire peut également être utilisé "
                u"dans les projets de type : "
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
        from autonomie.models.project.phase import SubProject
        return SubProject.query().filter_by(
            subproject_type_id=self.id
        ).count() > 0
