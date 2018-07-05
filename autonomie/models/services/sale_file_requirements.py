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
from sqlalchemy import or_
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
        if node.project is not None:
            for indicator in node.file_requirements:
                if indicator.requirement_type == 'project_mandatory':
                    for file_object in node.project.files:
                        if file_object.file_type_id == indicator.file_type_id:
                            indicator.set_file(file_object.id)
                    if hasattr(node, "business_id"):
                        business_id = node.business_id
                        task_id = node.id
                    else:  # it's a business
                        business_id = node.id
                        task_id = None

                    for existing in cls.query_existing_project_indicators(
                        node.project_id,
                        indicator.file_type_id,
                        task_id=task_id,
                        business_id=business_id
                    ):
                        indicator.merge_indicator(existing)

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
            if action == 'add':
                cls.on_file_add(node, file_object)
            elif action == 'update':
                cls.on_file_update(node, file_object)
            elif action == "delete":
                cls.on_file_remove(node, file_object)

    @classmethod
    def _get_invalid_indicators(cls, node):
        """
        Collect indicators attached to node that are not successfully validate

        :param obj node: The associated node
        """
        result = SaleFileRequirement.query().filter_by(
            node_id=node.id
        ).filter(
            SaleFileRequirement.status !=
            SaleFileRequirement.SUCCESS_STATUS
        ).filter_by(forced=False)
        return result.all()

    @classmethod
    def get_mandatory_indicators(cls, task_id, file_type_id):
        """
        Update mandatory indicator types
        """
        result = SaleFileRequirement.query().filter_by(
            node_id=task_id
        ).filter_by(
            file_type_id=file_type_id
        ).filter(
            SaleFileRequirement.requirement_type.in_(
                (
                    BusinessTypeFileType.MANDATORY,
                    BusinessTypeFileType.RECOMMENDED,
                )
            )
        ).all()
        return result

    @classmethod
    def query_existing_business_indicators(
        cls, business_id, file_type_id, task_id=None
    ):
        """
        Build a query for indicators related to a given business
        Excludes indicators related to task_id

        :param int business_id: The business id
        :param int file_type_id: The type of file the indicators are related to
        :param int task_id: The id of the task to exclude from the query
        """
        from autonomie.models.task import Task
        tasks_id_query = DBSESSION().query(Task.id).filter_by(
            business_id=business_id
        )
        if task_id is not None:
            tasks_id_query = tasks_id_query.filter(Task.id != task_id)

        query = SaleFileRequirement.query().filter_by(
            file_type_id=file_type_id
        )
        return query.filter(
            or_(
                SaleFileRequirement.node_id == business_id,
                SaleFileRequirement.node_id.in_(tasks_id_query)
            )
        )

    @classmethod
    def query_existing_project_indicators(
        cls, project_id, file_type_id, task_id=None, business_id=None
    ):
        """
        Build a query for indicators related to a given project
        Excludes indicators related to task_id

        :param int project_id: The Project id
        :param int file_type_id: The type of file the indicators are related to
        :param int task_id: The id of the task to exclude from the query
        :param int business_id: The id of the business to exclude from the query
        """
        from autonomie.models.task import Task
        from autonomie.models.project.business import Business
        tasks_id_query = DBSESSION().query(Task.id).filter_by(
            project_id=project_id
        )
        if task_id:
            tasks_id_query = tasks_id_query.filter(Task.id != task_id)

        businesses_id_query = DBSESSION().query(Business.id).filter_by(
            project_id=project_id
        )
        if business_id:
            businesses_id_query = businesses_id_query.filter(
                Business.id != business_id
            )
        query = SaleFileRequirement.query().filter_by(
            file_type_id=file_type_id
        )
        return query.filter(
            or_(
                SaleFileRequirement.node_id.in_(businesses_id_query),
                SaleFileRequirement.node_id.in_(tasks_id_query),
            )
        )

    @classmethod
    def get_business_mandatory_indicators(cls, business_id, file_type_id):
        """
        Update business_mandatory and under indicator types
        """
        query = cls.query_existing_business_indicators(
            business_id, file_type_id
        )
        query = query.filter_by(
            requirement_type=BusinessTypeFileType.BUSINESS_MANDATORY
        )
        return query.all()

    @classmethod
    def get_project_mandatory_indicators(cls, project_id, file_type_id):
        """
        Update project_mandatory and under indicator types
        """
        query = cls.query_existing_project_indicators(
            project_id, file_type_id
        )
        query = query.filter_by(
            requirement_type=BusinessTypeFileType.PROJECT_MANDATORY
        )
        return query.all()

    @classmethod
    def get_file_related_indicators(cls, file_id):
        """
        Return indicators related to the given file object
        """
        return SaleFileRequirement.query().filter_by(file_id=file_id).all()

    @classmethod
    def on_file_add(cls, node, file_object):
        for indicator in cls.get_related_indicators(
            node,
            file_object.file_type_id
        ):
            indicator.set_file(file_object.id)

    @classmethod
    def on_file_update(cls, node, file_object):
        for indicator in cls.get_related_indicators(
            node,
            file_object.file_type_id
        ):
            indicator.update_file(file_object.id)

    @classmethod
    def on_file_remove(cls, node, file_object):
        for indicator in cls.get_file_related_indicators(
            file_object.id
        ):
            print("  Indicator : %s" % indicator)
            indicator.remove_file()

    @classmethod
    def force_all(cls, node):
        """
        Force all indicators that are not successfull

        :param obj node: The associated node
        """
        for indicator in cls._get_invalid_indicators(node):
            indicator.force()
            DBSESSION().merge(indicator)

    @classmethod
    def check(cls, node):
        """
        Check if all indicators are successfull
        :param obj node: The node for which we check the indicators
        """
        query = DBSESSION().query(SaleFileRequirement.id)
        query = query.filter_by(node_id=node.id)
        query = query.filter(
            SaleFileRequirement.status != SaleFileRequirement.SUCCESS_STATUS
        )
        return query.count() == 0


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
        if task.business_id is not None:
            for indicator in task.file_requirements:
                if indicator.requirement_type in (
                    'business_mandatory',
                    'project_mandatory'
                ):
                    for existing in cls.query_existing_business_indicators(
                        task.business_id,
                        indicator.file_type_id,
                        task_id=task.id
                    ):
                        indicator.merge_indicator(existing)

    @classmethod
    def get_related_indicators(cls, node, file_type_id):
        indicators = cls.get_mandatory_indicators(
            node.id, file_type_id
        )
        indicators.extend(
            cls.get_business_mandatory_indicators(
                node.business_id, file_type_id
            )
        )
        indicators.extend(
            cls.get_project_mandatory_indicators(node.project_id, file_type_id)
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
    def get_related_indicators(cls, node, file_type_id):
        indicators = cls.get_business_mandatory_indicators(
            node.id, file_type_id
        )
        indicators.extend(
            cls.get_project_mandatory_indicators(node.project_id, file_type_id)
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
    def get_related_indicators(cls, node, file_type_id):
        indicators = cls.get_project_mandatory_indicators(
            node.id, file_type_id
        )
        return indicators
