# -*- coding: utf-8 -*-
# * File Name : invoice.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 06-05-2012
# * Last Modified :
#
# * Project :
#
import logging
import datetime
from sqlalchemy import func
from autonomie.models.model import Invoice
from autonomie.models.model import ManualInvoice
from autonomie.models.model import format_to_taskdate


log = logging.getLogger(__name__)

def get_nextInvoiceNumber(dbsession):
    """
        Returns the next available invoice number
        @param dbsession:an instanciated session object
    """
    current_year = datetime.date.today().year
    year_start = int("{0}0101".format(current_year))
    lastinvoice = dbsession.query(func.max(Invoice.officialNumber)
                    ).filter(Invoice.taskDate>year_start).one()
    lastmanualinvoice = dbsession.query(func.max(ManualInvoice.officialNumber)
                    ).filter(ManualInvoice.taskDate>year_start).one()
    return max(lastinvoice.officialNumber, lastmanualinvoice.officialNumber)

