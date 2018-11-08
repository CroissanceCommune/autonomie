# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.utils.widgets import Link
from autonomie.utils.strings import format_account

from autonomie.models.project.business import Business
from autonomie.models.project.project import Project
from autonomie.forms.training.training import get_training_list_schema

from .lists import GlobalTrainingListView
from .routes import (
    TRAINING_DASHBOARD_URL,
    USER_TRAINER_EDIT_URL,
)


class TrainingDashboardView(GlobalTrainingListView):
    """
    Dashboard view allowing an employee to have an overview of its training
    activity

    Context : Company instance
    """
    is_admin = False
    schema = get_training_list_schema(is_admin=False)
    title = u"Mon activité de formation"

    def filter_company_id(self, query, appstruct):
        query = query.join(Business.project)
        query = query.filter(Project.company_id == self.context.id)
        return query

    def _trainer_datas_links(self):
        result = []
        for user in self.context.employees:
            if not self.request.has_permission('edit.trainerdatas', user):
                # Je ne peux pas éditer les infos formateurs de mes collègues
                continue

            if user.id == self.request.user.id:
                label = u"Voir ma fiche formateur"
            else:
                label = u"Voir la fiche formateur de {}".format(
                    format_account(user)
                )
            result.append(
                Link(
                    self.request.route_path(
                        USER_TRAINER_EDIT_URL,
                        id=user.id
                    ),
                    label,
                    icon="fa fa-search",
                    popup=True,
                    css='btn btn-default',
                )
            )
        return result

    def more_template_vars(self, result):
        result = GlobalTrainingListView.more_template_vars(self, result)
        result["trainer_datas_links"] = self._trainer_datas_links()
        return result


def includeme(config):
    config.add_view(
        TrainingDashboardView,
        route_name=TRAINING_DASHBOARD_URL,
        renderer="autonomie:/templates/training/dashboard.mako",
        permission="list.training",
    )
