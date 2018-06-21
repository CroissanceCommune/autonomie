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


def build_indicator_from_requirement_def(business_type_file_type_req):
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


class SaleFileRequirementService(object):

    @classmethod
    def populate(cls, node):
        """
        Generate SaleFileRequirement instances for the given node

        :param obj node: A :class:`autonomie.models.node.Node` instance
        related to the sale module
        """
        business_type_id = node.business_type_id
        if business_type_id is None:
            raise Exception(
                u"The provided Node instance %s has no business_type_id "
                u"set" % node
            )

        business_file_req_defs = BusinessTypeFileType.get_file_requirements(
            business_type_id, node.type_,
        )

        for business_file_req_def in business_file_req_defs:
            requirement = build_indicator_from_requirement_def(
                business_file_req_def,
            )
            node.file_requirements.append(requirement)

        cls.on_populate(node)
        return node

    @classmethod
    def on_populate(cls, node):
        pass

    @classmethod
    def check_project_files(cls, node):
        """
        Update file requirements regarding the project attached to the given
        node

        :param obj node: A :class:`autonomie.models.node.Node` instance
        """
        # FIXME : dans les checks, on devrait regarder si les requirements
        # requierent aussi validation, si oui, ça va devenir compliqué.
        # Peut être devrait-on oublié la partie validation ?

        if node.project is not None:
            for indicator in node.file_requirements:
                if indicator.requirement_type == 'project_mandatory':
                    for file_object in node.project.files:
                        if file_object.file_type_id == indicator.file_type_id:
                            indicator.set_file(file_object.id)

    @classmethod
    def register(cls, node, file_object, action="add"):
        """
        Update the Indicators attached to node if one is matching the
        file_object

        :param obj node: A :class:`autonomie.models.node.Node` instance
        related to the sale module
        :param obj file_object: A :class:`autonomie.models.files.File` instance
        that has juste been uploaded
        :param str action: add/update/delete
        """
        # TODO : alerté les niveaux supérieurs (business/project)
        # NB : si on a un update d'un fichier qui requiert validation, on doit
        # mettre à jour l'info sur les autres indicateurs
        if file_object.file_type_id:
            if action in ('add', 'update'):
                cls.on_file_add(node, file_object)
            elif action == "delete":
                cls.on_file_remove(node, file_object)

    @classmethod
    def get_mandatory_indicators(cls, task_id, file_object):
        """
        Update mandatory indicator types
        """
        result = SaleFileRequirement.query().filter_by(
            node_id=task_id
        ).filter_by(
            file_type_id=file_object.file_type_id
        ).filter_by(
            requirement_type=BusinessTypeFileType.MANDATORY
        ).all()
        return result

    @classmethod
    def get_business_mandatory_indicators(cls, business_id, file_object):
        """
        Update business_mandatory and under indicator types
        """
        from autonomie.models.task import Task
        result = SaleFileRequirement.query().filter_by(
            node_id=business_id
        ).filter_by(
            file_type_id=file_object.file_type_id
        ).all()

        task_ids = [i[0] for i in DBSESSION().query(Task.id).filter_by(
            business_id=business_id
        )]
        task_indicators = SaleFileRequirement.query().filter(
            SaleFileRequirement.node_id.in_(task_ids)
        ).filter_by(
            file_type_id=file_object.file_type_id
        ).filter_by(
            requirement_type=BusinessTypeFileType.BUSINESS_MANDATORY
        ).all()
        result.extend(task_indicators)
        return result

    @classmethod
    def get_project_mandatory_indicators(cls, project_id, file_object):
        """
        Update project_mandatory and under indicator types
        """
        from autonomie.models.task import Task
        business_ids = [
            i[0] for i in DBSESSION().query(Task.id).filter_by(
                project_id=project_id
            )
        ]
        result = SaleFileRequirement.query().filter(
            SaleFileRequirement.node_id.in_(business_ids)
        ).filter_by(
            requirement_type=BusinessTypeFileType.PROJECT_MANDATORY
        ).all()

        task_ids = [i[0] for i in DBSESSION().query(Task.id).filter_by(
            project_id=project_id
        )]
        task_indicators = SaleFileRequirement.query().filter(
                SaleFileRequirement.node_id.in_(task_ids)
            ).filter_by(
                file_type_id=file_object.file_type_id
            ).filter_by(
                requirement_type=BusinessTypeFileType.PROJECT_MANDATORY
            ).all()
        result.extend(task_indicators)
        return result

    @classmethod
    def on_file_add(cls, node, file_object):
        for indicator in cls.get_related_indicators(node, file_object):
            indicator.set_file(file_object)

    @classmethod
    def on_file_remove(cls, node, file_object):
        for indicator in cls.get_related_indicators(node, file_object):
            indicator.remove_file(file_object)


class TaskFileRequirementService(SaleFileRequirementService):

    @classmethod
    def on_populate(cls, node):
        cls.check_business_files(node)
        cls.check_project_files(node)
        return node

    @classmethod
    def check_business_files(cls, task):
        """
        Update file requirements regarding the business attached to the given
        task

        :param obj task: A :class:`autonomie.models.node.Node` instance
        """
        if task.business is not None:
            for indicator in task.file_requirements:
                if indicator.requirement_type in (
                    'business_mandatory',
                    'project_mandatory'
                ):
                    for file_req in task.business.file_requirements:
                        if file_req.file_type_id == indicator.file_type_id:
                            indicator.merge_indicator(file_req)

    @classmethod
    def get_related_indicators(cls, node, file_object):
        indicators = cls.get_mandatory_indicators(
            node.id, file_object
        )
        indicators.extend(
            cls.get_business_mandatory_indicators(
                node.business_id, file_object
            )
        )
        indicators.extend(
            cls.get_project_mandatory_indicators(node.project_id, file_object)
        )
        return indicators


class BusinessFileRequirementService(SaleFileRequirementService):
    """
    Manage Business file requirements
    """

    @classmethod
    def on_populate(cls, node):
        cls.check_task_files(node)
        cls.check_project_files(node)
        return node

    @classmethod
    def check_task_files(cls, business):
        for task in business.tasks:
            for indicator in business.file_requirements:
                for file_req in task.file_requirements:
                    if file_req.file_type_id == indicator.file_type_id:
                        indicator.merge_indicator(file_req)

    @classmethod
    def get_related_indicators(cls, node, file_object):
        indicators = cls.get_business_mandatory_indicators(
            node.id, file_object
        )
        indicators.extend(
            cls.get_project_mandatory_indicators(node.project_id, file_object)
        )
        return indicators


class ProjectFileRequirementService(SaleFileRequirementService):
    """
    Manage Project file requirements
    """

    @classmethod
    def populate(cls, node):
        return node

    @classmethod
    def get_related_indicators(cls, node, file_object):
        indicators = cls.get_project_mandatory_indicators(
            node.id, file_object
        )
        return indicators
