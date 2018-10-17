# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models.task import Task
from autonomie.models.project.business import Business
from autonomie.views.indicators import INDICATOR_ROUTE
from autonomie.panels.files import stream_actions


def sale_file_requirements_panel(context, request, file_requirements):
    """
    Show the file requirements indicators for the given context
    """
    if isinstance(context, Task):
        file_add_route = "/%ss/{id}/addfile" % (context.type_,)
    elif isinstance(context, Business):
        file_add_route = "/businesses/{id}/addfile"

    file_add_url = request.route_path(
        file_add_route,
        id=context.id,
    )

    return dict(
        indicators=file_requirements,
        stream_actions=stream_actions,
        file_add_url=file_add_url,
        force_route=INDICATOR_ROUTE,
    )


def custom_indicator_panel(context, request, indicator):
    """
    Panel displaying an indicator in a generic format
    """
    force_url = request.route_path(
        INDICATOR_ROUTE,
        id=indicator.id,
        _query={'action': 'force'},
    )
    return dict(indicator=indicator, force_url=force_url)


def includeme(config):
    TEMPLATE_PATH = "autonomie:templates/panels/indicators/{}"
    config.add_panel(
        sale_file_requirements_panel,
        "sale_file_requirements",
        renderer=TEMPLATE_PATH.format("sale_file_requirements.mako"),
    )
    config.add_panel(
        custom_indicator_panel,
        "custom_indicator",
        renderer=TEMPLATE_PATH.format("custom_indicator.mako")
    )
