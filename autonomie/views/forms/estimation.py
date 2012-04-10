# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 09-04-2012
# * Last Modified :
#
# * Project :
#
"""
    Estimation form schema
    Note : since deform doesn't fit our form needs
            (estimation form is complicated and its structure
             is mixing many sqla tables)

    validation process:
        set all the line in the colander expected schema
        validate
        raise error on an adapted way
            build an error dict which is mako understandable

    merging process:
        get the datas
        build a factory
        merge estimation and task object
        commit
        merge all lines
        commit
        merge payment conditions
        commit
"""
import logging
import colander

from deform import ValidationFailure

from autonomie.models import DBSESSION
from autonomie.models.model import Estimation
from autonomie.models.model import EstimationLine
#from autonomie.models import Task
#from autonomie.models import PaymentConditions

log = logging.getLogger(__name__)

class EstimationFormSchema():
    """
        colander Schema for validating the estimation form
    """
    pass

def collect_indexes(keys, identifier):
    """
        return estimation line indexes
    """
    return [int(key[len(identifier):]) for key in keys if key.startswith(identifier)]

def format_lines(datas):
    """
        get all the estimation lines configured in datas and
        return a colander friendly data structure
    """
    keys = datas.keys()
    # keys :
    # prestation_id
    # price_id
    # quantity_id
    # unity_id
    indexes = collect_indexes(keys, "prestation_")
    lines = []
    for index in indexes:
        prestation = datas['prestation_%d' % index]
        quantity = datas['quantity_%d' % index]
        price = datas['price_%d' % index]
        unity = datas['unity_%d' % index]
        lines.append(dict(description=prestation,
                          cost=price,
                          quantity=quantity,
                          unity=unity))
    return lines

def format_task(datas):
    """
        return all the task related fields
    """
    keys = ['id_phase','description','taskDate',]
    return dict((key, datas.get(key)) for key in keys)

def format_estimation(datas):
    """
        return the estimation related fields
    """
    keys = ["tva",
            "deposit",
            "paymentConditions",
            "exclusions",
            "course",
            "displayedUnits",
            "discountHT",
            "expenses",
            "paymentDisplay",]
    return dict((key, datas.get(key)) for key in keys)

def format_payment_conditions(datas):
    """
        format all payment conditions related datas
        to fit colander schema's expected structure
    """
    keys = datas.keys()
    payments = []
    indexes = collect_indexes(keys, "description_")
    indexes.sort()
    for index in indexes:
        description = datas["description_%d" % index]
        amount = datas["amount_%d" % index]
        paymentDate = datas["paymentDate_%s" % index]
        payments.append(dict(description=description,
                             amount=amount,
                             paymentDate=paymentDate,
                             rowIndex=index))
    return payments

def format_datas(datas):
    """
        format all estimation form datas to fit the colander schema
    """
    log.debug("Formatting datas : %s" % (datas,))
    tovalid = dict(estimation=format_estimation(datas),
                   task=format_task(datas),
                   estimation_lines=format_lines(datas),
                   payment_conditions=format_payment_conditions(datas),
                   )
    return tovalid

class EstimationForm():
    """
        Estimation Form makes the glue beetween
        colander (form validation),
        sqla (database orm)
        user-input
        user inputted datas are formatted;
        sent to colander;
        once validated, returns the appropriate elements
        to insert into the database
    """
    def __init__(self, schema):
        self.schema = schema

    def validate(self, datas):
        """
            Launch datas validation
        """
        cstruct = format_datas(datas)
        try:
            validated = self.schema.deserialize(cstruct)
        except colander.Invalid, e:
            errors = e.asdict()
            log.warn(errors)
            raise ValidationFailure(errors)
        return validated

def get_estimation_line(lines, _id):
    """
        Return an estimation_line object matching the _id
    """
    for line in lines:
        if line['id'] == _id:
            return line
    return EstimationLine()

def merge_line(line, estimation_lines):
    """
        Merge a line with an estimation_line sqla object if needed
    """
    pass

def merge_appstruct_todatabase(datas, task=None,
                                      estimation=None,
                                      estimation_lines=[],
                                      payment_conditions=None):
    """
        Build/update sqla elements from validated datas
        Input : datas and sqla objects
        Output : updated sqla objects
        Note: find a way to match estimation_lines with workline ids
    """
    estimation.name = datas['estimation']['name']
    for line in datas['estimation_line']:
        if line.has_key('idworkline'):
            merge_line(line, estimation_lines)
