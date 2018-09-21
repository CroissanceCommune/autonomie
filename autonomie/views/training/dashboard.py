# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.utils.widgets import Link
from autonomie.utils.strings import format_account

from autonomie.views import BaseView
from .routes import (
    TRAINING_DASHBOARD_URL,
    USER_TRAINER_EDIT_URL,
)


class TrainingDashboardView(BaseView):
    """
    Dashboard view allowing an employee to have an overview of its training
    activity

    Context : Company instance
    """

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

    def __call__(self):
        return dict(
            trainer_datas_links=self._trainer_datas_links(),
        )


def includeme(config):
    config.add_view(
        TrainingDashboardView,
        route_name=TRAINING_DASHBOARD_URL,
        renderer="autonomie:/templates/training/dashboard.mako",
        permission="list.training",
    )
