# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def link_panel(context, request):
    """
    simple link panel used to render links

    :param obj context: The context to render, an instance of the Button class
    :param obj request: The current pyramid request
    """
    return dict(link=context)


def menu_dropdown_panel(context, request, label, links):
    """
    Menu dropdown panel

    :param obj context: The current context
    :param obj request: The current pyramid request
    :param str label: the label to use
    :param list buttons: List of autonomie.widgets.Link
    """
    return dict(label=label, links=links)


def includeme(config):
    config.add_panel(
        link_panel,
        "link",
        renderer="autonomie:templates/panels/widgets/link.pt",
    )
    config.add_panel(
        menu_dropdown_panel,
        "menu_dropdown",
        renderer="autonomie:templates/panels/widgets/menu_dropdown.pt",
    )
