# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
User page sidebar menu panels
"""


def sidebar_panel(context, request, menu):
    """
    Collect datas for menu display

    :param obj context: The current context
    :param request: The current request object
    :param obj menu: An instance of utils.menu.Menu
    """
    return {
        'menu': menu,
        'current': menu.current or context,
    }


def sidebar_item_panel(context, request, menu_item, bind_params):
    """
    Collect datas for menu entry display

    :param obj context: The current context
    :param request: The current request object
    :param obj menu_item: An instance of utils.menu.MenuItem or
    utils.menu.MenuDropdown
    :param dict bind_params: Binding parameters attached to the parent menu and
    used to dynamically render some attributes
    """
    return {
        "menu_item": menu_item,
        "bind_params": bind_params,
    }


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    config.add_panel(
        sidebar_panel,
        'sidebar',
        renderer='/panels/sidebar.mako',
    )
    config.add_panel(
        sidebar_item_panel,
        'sidebar_item',
        renderer='/panels/sidebar_item.mako',
    )
