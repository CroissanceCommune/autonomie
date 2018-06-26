# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie_base.models.base import DBSESSION


class FindCompanyService(object):
    """
    Tools used to retrieve company informations like :

        employee logins

        find company from node
    """
    @classmethod
    def find_company_id_from_node(cls, node_instance):
        if hasattr(node_instance, "company_id"):
            return node_instance.company_id

        if hasattr(node_instance, "project_id"):
            from autonomie.models.project import Project
            return DBSESSION().query(
                Project.company_id
            ).filter_by(id=node_instance.project_id).scalar()

    @classmethod
    def find_employees_login_from_node(cls, node_instance):
        from autonomie.models.company import Company
        from autonomie.models.user.user import User
        from autonomie.models.user.login import Login
        cid = cls.find_company_id_from_node(node_instance)
        query = DBSESSION().query(Login.login).join(
            Login.user
        ).join(
            User.companies
        ).filter(Company.id == cid)
        return [u[0] for u in query]
