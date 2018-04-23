# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from autonomie.views.user.routes import USER_ITEM_URL


USERDATAS_URL = "/userdatas"
USERDATAS_XLS_URL = "/userdatas.xls"
USERDATAS_CSV_URL = "/userdatas.csv"
USERDATAS_ODS_URL = "/userdatas.ods"
USERDATAS_ITEM_URL = os.path.join(USERDATAS_URL, "{id}")
USERDATAS_EDIT_URL = os.path.join(USERDATAS_ITEM_URL, "edit")
USERDATAS_DOCTYPES_URL = os.path.join(USERDATAS_ITEM_URL, "doctypes")
USERDATAS_PY3O_URL = os.path.join(USERDATAS_ITEM_URL, "py3o")
USERDATAS_MYDOCUMENTS_URL = os.path.join(USERDATAS_ITEM_URL, "mydocuments")
USERDATAS_FILELIST_URL = os.path.join(USERDATAS_ITEM_URL, "filelist")
USERDATAS_HISTORY_URL = os.path.join(USERDATAS_ITEM_URL, "history")

USER_USERDATAS_URL = os.path.join(USER_ITEM_URL, "userdatas")
USER_USERDATAS_ADD_URL = os.path.join(USER_USERDATAS_URL, "add")
USER_USERDATAS_EDIT_URL = os.path.join(USER_USERDATAS_URL, "edit")
USER_USERDATAS_DOCTYPES_URL = os.path.join(USER_USERDATAS_URL, "doctypes")
USER_USERDATAS_PY3O_URL = os.path.join(USER_USERDATAS_URL, "py3o")
USER_USERDATAS_MYDOCUMENTS_URL = os.path.join(USER_USERDATAS_URL, "mydocuments")
USER_USERDATAS_FILELIST_URL = os.path.join(USER_USERDATAS_URL, "filelist")
USER_USERDATAS_HISTORY_URL = os.path.join(USER_USERDATAS_URL, "history")

TEMPLATING_URL = "/templatinghistory"
TEMPLATING_ITEM_URL = os.path.join(TEMPLATING_URL, '{id}')


def includeme(config):
    for route in (
        USERDATAS_URL, USERDATAS_XLS_URL, USERDATAS_CSV_URL, USERDATAS_ODS_URL
    ):
        config.add_route(route, route)

    for route in (
        USERDATAS_ITEM_URL, USERDATAS_EDIT_URL, USERDATAS_DOCTYPES_URL,
        USERDATAS_PY3O_URL, USERDATAS_MYDOCUMENTS_URL, USERDATAS_FILELIST_URL,
        USERDATAS_HISTORY_URL
    ):
        config.add_route(route, route, traverse="/userdatas/{id}")

    for route in (
        USER_USERDATAS_URL, USER_USERDATAS_ADD_URL, USER_USERDATAS_EDIT_URL,
        USER_USERDATAS_DOCTYPES_URL, USER_USERDATAS_PY3O_URL,
        USER_USERDATAS_MYDOCUMENTS_URL, USER_USERDATAS_FILELIST_URL,
        USER_USERDATAS_HISTORY_URL
    ):
        config.add_route(route, route, traverse="/users/{id}")

    config.add_route(TEMPLATING_URL, TEMPLATING_URL)
    config.add_route(
        TEMPLATING_ITEM_URL,
        TEMPLATING_ITEM_URL,
        traverse="/templatinghistory/{id}"
    )
