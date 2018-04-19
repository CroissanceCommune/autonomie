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

    result['help_message'] = parent_tmpl_dict.get(
        'help_message',
        parent_tmpl_dict.get('help_msg')
    )
    result['warn_message'] = parent_tmpl_dict.get('warn_message')
    result['info_message'] = parent_tmpl_dict.get('info_message')
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
