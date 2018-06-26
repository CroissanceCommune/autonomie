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
    DBSESSION,
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
        self.status = "success"

    @property
    def validated(self):
        return self.validation_status == 'valid' or self.forced


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
        primaryjoin="SaleFileRequirement.file_id==File.id",
        backref="sale_requirements",
    )
    node = relationship(
        "Node",
        primaryjoin="SaleFileRequirement.node_id==Node.id",
        backref="file_requirements",
    )
    file_type = relationship("FileType")

    def __init__(self, *args, **kwargs):
        Indicator.__init__(self, *args, **kwargs)
        self.set_default_status()
        self.set_default_validation_status()

    def set_default_status(self):
        """
        Set the default status regarding the requirement type
        """
        if self.requirement_type == 'recommended':
            self.status = 'warning'
        else:
            self.status = 'danger'

    def set_default_validation_status(self):
        """
        Set the default validation status regarding the validation attribute
        """
        if not self.validation:
            self.validation_status = 'valid'
        else:
            self.validation_status = 'none'

    def merge_indicator(self, indicator):
        """
        Merge the given SaleFileRequirement with the current one

        if a file has been provided, we call the set_file method that handles
        the status
        if no file has been provided, the indicator may have been forced, we
        register that status

        :param obj indicator: an instance of the current class
        """
        result = self
        # on a un fichier
        if indicator.file_id is not None:
            result = self.set_file(
                indicator.file_id,
                validated=indicator.validated,
            )
            # on récupère l'état de validation du fichier déposé
            if indicator.validation == self.validation:
                self.validation_status = indicator.validation_status

        return result

    def set_file(self, file_id, validated=False):
        """
        Attach a file_id to this indicator

        :param int file_id: An id of a file persisted to database
        :param bool validated: True if this file been validated in another
        indicator
        """
        self.file_id = file_id
        if not validated and self.validation:
            self.validation_status = 'wait'
            self.status = 'warning'
        else:
            self.status = 'success'
        return DBSESSION().merge(self)

    def update_file(self, file_id):
        """
        The file file_id was updated, we update the indicator if it was related
        to this file and if needed (if the current requirement needs validation)

        :param int file_id: An id of a file persisted to database
        :param bool validated: True if this file been validated in another
        indicator
        """
        if self.file_id == file_id and self.validation:
            self.validation_status = 'wait'
            self.status = 'warning'
            DBSESSION().merge(self)

    def remove_file(self):
        """
        Remove file reference from this indicator
        """
        self.file_id = None
        self.set_default_status()
        self.set_default_validation_status()
        return DBSESSION().merge(self)
