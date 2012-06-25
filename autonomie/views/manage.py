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

from pyramid.view import view_config

from autonomie.models.model import Invoice, Estimation

log = logging.getLogger(__name__)

@view_config(route_name="manage", renderer="manage.mako", permission="manage")
def manage(request):
    """
        The manage view
    """
    dbsession = request.dbsession()
    invoices = Invoice.query(dbsession).filter(Invoice.CAEStatus=='wait').all()
    for i in invoices:
        i.url = request.route_path("invoice", id=i.id)

    estimations = Estimation.query(dbsession).filter(
                                       Estimation.CAEStatus=='wait').all()
    for i in estimations:
        i.url = request.route_path("estimation", id=i.id)
    invoices.extend(estimations)
    invoices = sorted(invoices, key=lambda a:a.statusDate)
    return dict(title=u"Documents en attente de validation",
                tasks=invoices,
               )

