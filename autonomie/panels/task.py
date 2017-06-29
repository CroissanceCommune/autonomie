# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#
"""

    Panels used for task rendering

"""


def task_panel(context, request, task, bulk=False):
    """
        Task panel
    """
    tvas = task.get_tvas()
    # Check if we've got multiple positive tvas in our task
    multiple_tvas = len([val for val in tvas if val > 0]) > 1
    return dict(
        task=task,
        project=task.project,
        company=task.project.company,
        multiple_tvas=multiple_tvas,
        tvas=tvas,
        config=request.config,
        bulk=bulk,
    )


STATUS_LABELS = {
    "wait": u"En attente de validation",
    "valid": {
        "estimation": u"En cours",
        "invoice": u"En attente de paiement",
        "cancelinvoice": u"Soldé",
        "expensesheet": u"Validée",
    },
    "aborted": u"Annulé",
    "signed": u"Signé par le client",
    "geninv": u"Factures générées",
    "paid": u"Payée partiellement",
    "resulted": u"Soldée",
    "justified": u"Justificatifs reçus",
}


def task_title_panel(context, request, title):
    """
    Panel returning a label for the given context's status
    """
    from autonomie.views import render_api
    status = render_api.major_status(context)
    status_label = STATUS_LABELS.get(status)
    if isinstance(status_label, dict):
        status_label = status_label[context.type_]

    icon = render_api.status_icon(context)

    css = u'status status-%s' % context.status
    if hasattr(context, 'paid_status'):
        css += u' paid-status-%s' % context.paid_status
        if hasattr(context, 'is_tolate'):
            css += u' tolate-%s' % context.is_tolate()
        elif hasattr(context, 'justified'):
            css += u' justified-%s' % context.justified
    elif hasattr(context, 'signed_status'):
        css += u' signed-status-%s geninv-%s' % (
            context.signed_status,
            context.geninv,
        )
    else:  # cancelinvoice
        if status == 'valid':
            css += ' paid-status-resulted'

    return dict(
        title=title,
        item=context,
        css=css,
        icon=icon,
        status_label=status_label
    )


def includeme(config):
    """
        Pyramid's inclusion mechanism
    """
    for document_type in ('estimation', 'invoice', 'cancelinvoice'):
        panel_name = "{0}_html".format(document_type)
        template = "panels/{0}.mako".format(document_type)
        config.add_panel(task_panel, panel_name, renderer=template)
    config.add_panel(
        task_title_panel,
        "task_title_panel",
        renderer="panels/task_title_panel.mako",
    )
