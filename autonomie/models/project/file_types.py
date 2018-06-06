# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
File types requirement models
"""
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)


class BusinessTypeFileType(DBBASE):
    """
    Relationship table between

    :class:`autonomie.models.project.types.BusinessType`
    and
    :class:`autonomie.models.files.FileType`
    """
    __tablename__ = "business_type_file_type"
    __table_args__ = default_table_args
    file_type_id = Column(ForeignKey("file_type.id"), primary_key=True)
    business_type_id = Column(ForeignKey("business_type.id"), primary_key=True)

    # estimation/invoice/cancelinvoice/business
    doctype = Column(String(14), primary_key=True)
    file_type = relationship(
        "FileType",
        backref=backref("business_type_rel", cascade='all, delete-orphan'),
    )
    business_type = relationship(
        "BusinessType",
        backref=backref("file_type_rel", cascade='all, delete-orphan'),
    )
    # global_mandatory / mandatory / optionnal / recommended
    requirement_type = Column(
        String(17),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Obligatoire ?",
            }
        },
    )
    validation = Column(
        Boolean(),
        default=False,
        info={
            "colanderalchemy": {
                "title": u"Validation équipe d'appui ?",
                "description": u"Ce document doit-il être validé par l'équipe "
                u"d'appui ?"
            }
        }
    )
