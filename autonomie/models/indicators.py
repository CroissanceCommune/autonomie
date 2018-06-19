# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
"""
import logging
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.orm import (
    relationship,
)

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)


logger = logging.getLogger(__name__)


class Indicator(DBBASE):
    """
    Model recording computed statuses
    """
    __tablename__ = 'indicator'
    __table_args__ = default_table_args
    __mapper_args__ = {
        'polymorphic_on': 'type_',
        'polymorphic_identity': 'indicator',
    }
    id = Column(Integer, primary_key=True)
    # danger / warning / success
    status = Column(String(20), default='danger')
    # none / invalid / wait / valid
    validation_status = Column(String(20), default='none')
    forced = Column(Boolean(), default=False)
    created_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Créé(e) le",
            }
        },
        default=datetime.now,
    )
    updated_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Mis(e) à jour le",
            }
        },
        default=datetime.now,
        onupdate=datetime.now
    )
    type_ = Column(
        'type_',
        String(30),
        info={'colanderalchemy': {'exclude': True}},
        nullable=False,
    )

    def force(self):
        self.forced = True


class SaleFileRequirement(Indicator):
    """
    Model recording File Requirements status
    """
    __tablename__ = 'sale_file_requirement'

    __mapper_args__ = {'polymorphic_identity': 'sale_file_requirement'}
    id = Column(ForeignKey("indicator.id"), primary_key=True)
    # Copied from the BusinessTypeFileType table
    file_type_id = Column(
        ForeignKey('file_type.id')
    )
    doctype = Column(String(14))
    requirement_type = Column(String(20))
    validation = Column(Boolean(), default=False)

    file_id = Column(ForeignKey("file.id"), nullable=True)
    node_id = Column(ForeignKey('node.id'))

    file_object = relationship(
        "File",
        primaryjoin="SaleFileRequirement.file_id==File.id"
    )
    node = relationship(
        "Node",
        primaryjoin="SaleFileRequirement.node_id==Node.id",
        backref="file_requirements",
    )
    file_type = relationship("FileType")
