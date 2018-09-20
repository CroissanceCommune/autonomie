# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import colander
from sqlalchemy import distinct
from sqlalchemy.orm import (
    selectinload,
    joinedload,
)

from autonomie.models.user.user import User
from autonomie.models.project.types import (
    BusinessType,
)
from autonomie.models.project.business import Business
from autonomie.models.task.task import Task
from autonomie.models.project import Project
from autonomie.models.customer import Customer
from autonomie.models.company import Company

from autonomie.forms.training.trainer import get_list_schema
from autonomie.forms.training.training import get_training_list_schema

from autonomie.utils.widgets import Link
from autonomie.views.user.lists import BaseUserListView
from autonomie.views import BaseListView
from autonomie.views.training.routes import (
    TRAINER_LIST_URL,
    TRAINING_LIST_URL,
)
from autonomie.views.business.routes import (
    BUSINESS_ITEM_ROUTE,
)


logger = logging.getLogger(__name__)


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
    add_template_vars = ('stream_columns', 'stream_actions',)

    def _get_training_business_type(self):
        """
        Retrieve the training project type id from the database
        """
        return self.dbsession.query(
            BusinessType.id
        ).filter_by(
            name="training"
        ).scalar() or -1

    def query(self):
        business_type_id = self._get_training_business_type()
        query = self.dbsession.query(
            distinct(Business.id), Business
        ).filter(
            Business.business_type_id == business_type_id
        )
        query = query.options(
            joinedload(Business.project).load_only('id').\
            selectinload(Project.company).load_only(
                Company.id, Company.name
            ),
            selectinload(Business.tasks).\
            selectinload(Project.customers).load_only(
                Customer.id, Customer.label
            )
        )
        return query

    def filter_company_id(self, query, appstruct):
        company_id = appstruct.get('company_id', None)
        if company_id not in (None, '', colander.null):
            logger.debug(u"  + Filtering on company_id")
            query = query.join(Business.project)
            query = query.filter(Project.company_id == company_id)
        return query

    def filter_customer_id(self, query, appstruct):
        customer_id = appstruct.get('customer_id', None)
        if customer_id not in (None, '', colander.null):
            logger.debug(u"  + Filtering on customer_id")
            query = query.outerjoin(Business.tasks)
            query = query.filter(
                Business.tasks.any(Task.customer_id == customer_id)
            )
        return query

    def filter_search(self, query, appstruct):
        search = appstruct.get('search', None)

        if search not in (None, colander.null, ''):
            logger.debug(u"  + Filtering on search")
            query = query.outerjoin(Business.tasks)
            query = query.filter(
                Project.tasks.any(
                    Task.official_number == search
                )
            )
        return query

    def filter_include_closed(self, query, appstruct):
        include_closed = appstruct.get('include_closed', False)
        if not include_closed:
            logger.debug(u"  + Filtering on businesses")
            query = query.filter(Business.closed == False)
        return query

    def stream_columns(self, item):
        yield "TODO"
        yield item.name
        yield item.project.company.name
        yield item.tasks[0].customer.label

    def stream_actions(self, item):
        yield Link(
            self.request.route_path(
                BUSINESS_ITEM_ROUTE,
                id=item.id,
            ),
            u"Voir la formation",
            icon="pencil"
        )
        yield Link(
            self.request.route_path(
                "customer",
                id=item.tasks[0].customer.id,
            ),
            u"Voir le client {}".format(item.tasks[0].customer.label),
            icon="pencil"
        )
        yield Link(
            self.request.route_path(
                "company",
                id=item.project.company.id,
            ),
            u"Voir l'enseigne {}".format(item.project.company.name),
            icon="pencil"
        )


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
