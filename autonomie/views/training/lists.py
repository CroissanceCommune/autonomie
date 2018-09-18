# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from sqlalchemy import distinct

from autonomie.models.user.user import User
from autonomie.models.project.types import (
    ProjectType,
)
from autonomie.models.project.business import Business
from autonomie.models.task.task import Task
from autonomie.models.project import Project
from autonomie.models.customer import Customer

from autonomie.forms.training.trainer import get_list_schema
from autonomie.forms.training.training import get_training_list_schema

from autonomie.views.user.lists import BaseUserListView
from autonomie.views import BaseListView
from autonomie.views.training.routes import (
    TRAINER_LIST_URL,
    TRAINING_LIST_URL,
)


class TrainerListView(BaseUserListView):
    """
    View listing Trainers
    """
    title = u"Liste des formateurs de la CAE (qui ont une fiche formateur)"
    schema = get_list_schema()

    def filter_trainer(self, query, appstruct):
        query = query.join(User.trainerdatas)
        return query


class GlobalTrainingListView(BaseListView):
    """
    View listing projects of type "trainings"

    Status
    Company
    Customers (?)
    CA
    Actions
    """
    title = u"Liste des formations dispensées dans la CAE"
    schema = get_training_list_schema(is_admin=True)

    def _get_training_project_type(self):
        """
        Retrieve the training project type id from the database
        """
        return self.dbession.query(
            ProjectType.id
        ).filter_by(
            name="training"
        ).scalar() or -1

    def query(self):
        ptype_id = self._get_training_project_type()
        query = self.dbsession.query(distinct(Project.id), Project).filter_by(
            project_type_id=ptype_id
        )
        query = query.outerjoin(Project.businesses)
        query = query.outerjoin(Project.company)
        query = query.outerjoin(Project.customers)
        return query

    def filter_company_id(self, query, appstruct):
        company_id = appstruct.get('company_id', None)
        if company_id not in (None, '', colander.null):
            query = query.filter(Project.company_id == company_id)
        return query

    def filter_customer_id(self, query, appstruct):
        customer_id = appstruct.get('customer_id', None)
        if customer_id not in (None, '', colander.null):
            query = query.filter(
                Project.customers.any(Customer.id == customer_id)
            )
        return query

    def filter_search(self, query, appstruct):
        search = appstruct.get('search', None)

        if search not in (None, colander.null, ''):
            query = query.filter(Task.official_number == search)
        return query

    def filter_include_closed(self, query, appstruct):
        include_closed = appstruct.get('include_closed', False)
        if not include_closed:
            query = query.filter(
                Project.businesses.any(Business.closed == False)
            )
        return query


def includeme(config):
    config.add_view(
        TrainerListView,
        route_name=TRAINER_LIST_URL,
        renderer="/training/lists.mako",
        permission="visit"
    )
    config.add_view(
        GlobalTrainingListView,
        route_name=TRAINING_LIST_URL,
        renderer="/training/list_trainings.mako",
        permission="admin_trainings"
    )
