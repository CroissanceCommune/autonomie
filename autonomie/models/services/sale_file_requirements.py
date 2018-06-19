# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Service managing file requirements :

    Businesses

    Tasks (Invoice, Estimation, CancelInvoice)
"""
from autonomie_base.models.base import DBSESSION
from autonomie.models.project.file_types import BusinessTypeFileType
from autonomie.models.indicators import SaleFileRequirement


class TaskFileRequirementService(object):

    @classmethod
    def _build_requirement(cls, business_type_file_type_req):
        """
        Initialize an indicator from the given req definition object
        :param obj business_type_file_type_req: A BusinessTypeFileType instance
        :rtype: :class:`autonomie.models.indicators.SaleFileRequirement`
        """
        return SaleFileRequirement(
            file_type_id=business_type_file_type_req.file_type_id,
            validation=business_type_file_type_req.validation,
            doctype=business_type_file_type_req.doctype,
            requirement_type=business_type_file_type_req.requirement_type
        )

    @classmethod
    def populate(cls, task):
        """
        Generate SaleFileRequirement instances for the given task

        :param obj task: A :class:`autonomie.models.node.Node` instance
        related to the sale module
        """
        business_type_id = task.business_type_id
        if business_type_id is None:
            raise Exception(
                u"The provided Node instance %s has no business_type_id "
                u"set" % task
            )

        business_file_req_defs = BusinessTypeFileType.get_file_requirements(
            business_type_id, task.type_,
        )

        for business_file_req_def in business_file_req_defs:
            requirement = cls._build_requirement(business_file_req_def)
            if not requirement.validation:
                requirement.validation_status = 'valid'

            if requirement.requirement_type == 'recommended':
                requirement.status = 'warning'

            task.file_requirements.append(requirement)

        cls.check_business_files(task)
        cls.check_project_files(task)

        return task

    @classmethod
    def check_business_files(cls, task):
        """
        Update file requirements regarding the business attached to the given
        task

        :param obj task: A :class:`autonomie.models.node.Node` instance
        """
        # FIXME : dans les checks, on devrait regarder si les requirements
        # requierent aussi validation, si oui, ça va devenir compliqué.
        # Peut être devrait-on oublié la partie validation ?

        if task.business is not None:
            for indicator in task.file_requirements:
                if indicator.requirement_type in (
                    'business_mandatory',
                    'project_mandatory'
                ):
                    for file_object in task.business.files:
                        if file_object.file_type_id == indicator.file_type_id:
                            cls._set_success(indicator, file_object)

    @classmethod
    def check_project_files(cls, task):
        """
        Update file requirements regarding the project attached to the given
        task

        :param obj task: A :class:`autonomie.models.node.Node` instance
        """
        # FIXME : dans les checks, on devrait regarder si les requirements
        # requierent aussi validation, si oui, ça va devenir compliqué.
        # Peut être devrait-on oublié la partie validation ?

        if task.project is not None:
            for indicator in task.file_requirements:
                if indicator.requirement_type in (
                    'project_mandatory'
                ):
                    for file_object in task.project.files:
                        if file_object.file_type_id == indicator.file_type_id:
                            cls._set_success(indicator, file_object)

    @classmethod
    def _get_task_file_requirements(cls, task, file_type_id):
        """
        Retrieve file requirements of a specific type attached to the given task

        :param obj task: A :class:`autonomie.models.node.Node` instance
        related to the sale module
        :param int file_type: The id of the FileType we're looking for
        """
        query = SaleFileRequirement.query().filter_by(node_id=task.id)
        return query.filter_by(file_type_id=file_type_id)

    @classmethod
    def _set_success(cls, indicator, file_object):
        """
        Set the success status on the given indicator associating it to the
        file_object
        """
        indicator.status = 'success'
        indicator.file_id = file_object.id
        return DBSESSION().merge(indicator)

    @classmethod
    def register(cls, task, file_object):
        """
        Update the Indicators attached to task if one is matching the
        file_object

        :param obj task: A :class:`autonomie.models.node.Node` instance
        related to the sale module
        :param obj file_object: A :class:`autonomie.models.files.File` instance
        that has juste been uploaded
        """
        # 1- Trouver l'indicateur qui matche le file_type_id de file_object
        # 2- Si c'est un indicateur qui demande validation on le met en wait
        # 3- Si c'est un indicateur qui est recommandé
        # 4- Remonter vers le business et faire le même genre de check
        if file_object.file_type_id:
            file_requirements = cls._get_task_file_requirements(
                task,
                file_object.file_type_id
            )
            for indicator in file_requirements:
                cls._set_success(indicator, file_object)
