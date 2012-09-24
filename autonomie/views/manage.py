# -*- coding: utf-8 -*-
# * File Name : manage.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 25-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Manage view :
        - last documents page
"""
import logging

from sqlalchemy import and_
from pyramid.view import view_config

from autonomie.models.model import Task, Invoice, Estimation, Phase, CancelInvoice

log = logging.getLogger(__name__)


@view_config(route_name="manage", renderer="manage.mako", permission="manage")
def manage(request):
    """
        The manage view
    """
    documents = Task.query()\
            .with_polymorphic([Invoice, CancelInvoice, Estimation])\
            .join(Task.phase)\
            .filter(and_(Task.CAEStatus=='wait', Phase.name!=None))\
            .order_by(Task.statusDate).all()
    for document in documents:
        document.url = request.route_path(document.type_, id=document.id)
    return dict(title=u"Documents en attente de validation",
                tasks=documents,
               )
