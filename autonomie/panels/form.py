# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
A form display panel

Display a form including messages
"""


def help_message_panel(context, request, parent_tmpl_dict):
    """
    Collect panel datas for rendering help/info/warn messages

    :param obj context: Auto-filled context (Pyramid original view context)
    :param obj request: The request object (auto-filled)
    :param dict parent_tmpl_dict: The parent template context dict
    """
    result = {}

    for key, other_key in (
        ('help_message', 'help_msg'),
        ('warn_message', 'warn_msg'),
        ('info_message', 'info_msg'),
        ('error_message', 'error_msg'),
    ):
        value = parent_tmpl_dict.get(key)
        if value is None:
            value = parent_tmpl_dict.get(other_key)
        result[key] = value

    return result


def includeme(config):
    """
    Implement Pyramid inclusion mechanism
    """
    config.add_panel(
        help_message_panel,
        name='help_message_panel',
        renderer='autonomie:templates/panels/help_message.pt'
    )
