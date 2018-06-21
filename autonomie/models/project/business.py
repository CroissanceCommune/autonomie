# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
)
from autonomie_base.models.base import (
    default_table_args,
)
from autonomie.models.node import Node
from autonomie.models.services.sale_file_requirements import (
    BusinessFileRequirementService,
)


class Business(Node):
    """
    Permet de :

        * Collecter les fichiers

        * Regrouper devis/factures/avoirs

        * Calculer le CA d'une affaire

        * Générer les factures

        * Récupérer le HT à dépenser

        * Des choses plus complexes en fonction du type de business

    Business.estimations
    Business.invoices
    Business.invoices[0].cancelinvoices
    """
    __tablename__ = "business"
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': "business"}
    file_requirement_service = BusinessFileRequirementService

    id = Column(
        Integer,
        ForeignKey('node.id'),
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}},
    )
    closed = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Cette affaire est-elle terminée ?"
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

    # Relations
    business_type = relationship(
        "BusinessType",
    )
    project = relationship(
        "Project",
        primaryjoin="Project.id == Business.project_id",
    )
    tasks = relationship(
        "Task",
        primaryjoin="Task.business_id==Business.id",
        back_populates="business"
    )
    estimations = relationship(
        "Task",
        back_populates="business",
        primaryjoin="and_(Task.business_id==Business.id, "
        "Task.type_=='estimation')",
    )
    invoices = relationship(
        "Task",
        back_populates="business",
        primaryjoin="and_(Task.business_id==Business.id, "
        "Task.type_.in_(('invoice', 'cancelinvoice')))"
    )
