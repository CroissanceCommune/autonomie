# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models.user.user import User
from autonomie.forms.training.trainer import get_list_schema
from autonomie.views.user.lists import BaseUserListView


class TrainerListView(BaseUserListView):
    """
    View listing Trainers
    """
    title = u"Liste des formateurs de la CAE (qui ont une fiche formateur)"
    schema = get_list_schema()

    def filter_trainer(self, query, appstruct):
        query = query.join(User.trainerdatas)
        return query


def includeme(config):
    config.add_view(
        TrainerListView,
        route_name="/trainers",
        renderer="/training/lists.mako",
        permission="visit"
    )
