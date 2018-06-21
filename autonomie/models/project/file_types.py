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
    load_only,
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
    # project_mandatory / business_mandatory / mandatory / optionnal /
    # recommended
    requirement_type = Column(
        String(20),
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
    PROJECT_MANDATORY = 'project_mandatory'
    BUSINESS_MANDATORY = "business_mandatory"
    MANDATORY = "mandatory"
    RECOMMENDED = "recommended"
    OPTIONNAL = "optionnal"

    # requirement qui implique un indicateur de statut
    STATUS_REQUIREMENT_TYPES = (
        PROJECT_MANDATORY,
        BUSINESS_MANDATORY,
        MANDATORY,
        RECOMMENDED,
    )

    @classmethod
    def get_file_requirements(cls, business_type_id, doctype, mandatory=False):
        """
        Collect file requirements related to a given business_type
        """
        query = cls.query().filter_by(business_type_id=business_type_id)
        query = query.filter_by(doctype=doctype)
        if mandatory:
            query = query.filter(
                cls.requirement_type.in_(cls.STATUS_REQUIREMENT_TYPES)
            )
        return query

    @classmethod
    def get_file_type_options(cls, business_type_id, doctype):
        """
        Collect FileTypes associated to (business_type_id, doctype)

        :param int business_type_id: The business type id
        :param str doctype: One of the available doctypes
        :returns: A :class:`sqlalchemy.orm.Query`
        """
        id_query = cls.query('file_type_id')
        id_query = id_query.filter_by(business_type_id=business_type_id)
        id_query = id_query.filter_by(doctype=doctype)
        ids = [i[0] for i in id_query]

        result = []
        if ids is not None:
            from autonomie.models.files import FileType
            query = FileType.query().options(load_only('id', 'label')).filter(
                FileType.id.in_(ids)
            )
            result = query.all()
        return result
