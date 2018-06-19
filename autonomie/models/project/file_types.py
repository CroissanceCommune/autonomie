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
    Integer,
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_type_id = Column(ForeignKey("file_type.id"))
    business_type_id = Column(ForeignKey("business_type.id"))

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
    # requirement qui implique un indicateur de statut
    STATUS_REQUIREMENT_TYPES = (
        'project_mandatory',
        'business_mandatory',
        'mandatory',
        'recommended',
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

    @classmethod
    def find(cls, file_type_id, btype_id, doctype):
        query = cls.query().filter_by(business_type_id=btype_id)
        query = query.filter_by(file_type_id=file_type_id)
        query = query.filter_by(doctype=doctype)
        return query.first()
