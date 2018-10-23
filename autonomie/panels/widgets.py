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


def menu_dropdown_panel(context, request, label, links, icon=None):
    """
    Menu dropdown panel

    :param obj context: The current context
    :param obj request: The current pyramid request
    :param str label: the label to use
    :param str icon: An optionnal icon to add
    :param list buttons: List of autonomie.widgets.Link
    """
    return dict(label=label, links=links, icon=icon)


def action_dropdown_panel(context, request, label=u"Actions", links=()):
    return menu_dropdown_panel(context, request, label, links)


def legend_panel(context, request, legends):
    """
    a legend panel shows a legend link with a dropdown div containing the
    legends

    :param obj context: The request's context
    :param obj request: The current Pyramid request
    :param list legends: List of 2-uples (status-css class, label)
    """
    return dict(context=context, request=request, legends=legends)


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
    config.add_panel(
        action_dropdown_panel,
        "action_dropdown",
        renderer="autonomie:templates/panels/widgets/menu_dropdown.pt",
    )
    config.add_panel(
        legend_panel,
        name="list_legend",
        renderer="autonomie:templates/panels/widgets/legend.pt",
    )
