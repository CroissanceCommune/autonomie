# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from autonomie.views.user.routes import USER_ITEM_URL


TRAINER_LIST_URL = "/trainers"
TRAINER_URL = '/trainerdatas'
TRAINER_ITEM_URL = os.path.join(TRAINER_URL, "{id}")
TRAINER_FILE_URL = os.path.join(TRAINER_ITEM_URL, "filelist")
USER_TRAINER_URL = os.path.join(USER_ITEM_URL, "trainerdatas")
USER_TRAINER_ADD_URL = os.path.join(USER_TRAINER_URL, "add")
USER_TRAINER_EDIT_URL = os.path.join(USER_TRAINER_URL, "edit")
USER_TRAINER_FILE_URL = os.path.join(USER_TRAINER_URL, "filelist")
TRAINING_LIST_URL = "/trainings"


def includeme(config):
    config.add_route(TRAINER_LIST_URL, TRAINER_LIST_URL)
    config.add_route(TRAINER_URL, TRAINER_URL)
    config.add_route(TRAINING_LIST_URL, TRAINING_LIST_URL)

    for route in TRAINER_ITEM_URL, TRAINER_FILE_URL:
        config.add_route(route, route, traverse="/trainerdatas/{id}")

    for route in (
        USER_TRAINER_URL, USER_TRAINER_ADD_URL, USER_TRAINER_EDIT_URL,
        USER_TRAINER_FILE_URL
    ):
        config.add_route(route, route, traverse="/users/{id}")
