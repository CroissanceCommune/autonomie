# -*- coding: utf-8 -*-
# * File Name : comptabilite.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 12-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    all comptability related views
"""
import datetime
import logging

from sqlalchemy import or_
from deform import ValidationFailure
from deform import Form

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from autonomie.models.model import OperationComptable
from autonomie.models.model import Company
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.views import submit_btn
from autonomie.views.forms import OperationSchema

from .base import ListView

log = logging.getLogger(__name__)


class Column(object):
    """
        Column object
    """
    def __init__(self, label, sortable_key=None, linkfunc=None, getfunc=None):
        self.label = label
        self.sortable_key = sortable_key
        self.linkfunc = linkfunc
        self.getfunc = getfunc

    def is_sortable(self):
        """
            Return True if the column is sortable
        """
        return self.sortable_key is not None

    def get_link(self, obj):
        """
            Return the link associated to the current cell
        """
        if self.linkfunc:
            return self.linkfunc(obj)
        else:
            return None

    def get_value(self, obj):
        """
            Return the column's value
        """
        if self.getfunc:
            return self.getfunc(obj)
        else:
            return None


class ComptabilityView(ListView):
    """
        All views related to the comptability
    """
    columns = ('date', 'montant', 'libelle')
    default_sort = 'date'
    default_direction = 'desc'

    def _get_operation_form(self, edit=False):
        """
            Return the operation edit/add form
        """
        companies = [(unicode(c.id), c.name)
                for c in Company.query([Company.id, Company.name]).all()]
        schema = OperationSchema().bind(choices=companies, edit=edit)
        form = Form(schema, buttons=(submit_btn,))
        return form

    @view_config(route_name="operations",
            renderer="comptability/operations.mako", permission='manage')
    def list(self):
        """
            list all operations
        """
        search, sort, direction, current_page, items_per_page = \
                                                self._get_pagination_args()

        query = self._get_operations()

        # Getting available options for searching
        all_operations = query.all()
        years = sorted( set([i.year for i in all_operations]) )
        companies = sorted( set([
            (i.company_id, i.company.name) for i in all_operations
                                ]))

        if search:
            query = self._filter_search(query, search)

        # Filtering the main search
        company_id = self.request.params.get('company')
        if company_id:
            query = self._filter_company(query, company_id)

        year = self.request.params.get('year')
        if year:
            query = self._filter_year(query, year)

        operations = query.order_by(sort + " " + direction).all()
        records = self._get_pagination(operations,
                                       current_page,
                                       items_per_page)

        form = self._get_operation_form()
        return dict(title=u"Opérations comptables",
                    operations=records,
                    companies=companies,
                    current_company=company_id,
                    years=years,
                    current_year=year,
                    html_form=form.render()
                    )

    def _get_operations(self):
        """
            Return all operations
        """
        return self.dbsession.query(OperationComptable).join(
                                    OperationComptable.company)

    @staticmethod
    def _filter_company(query, company_id):
        """
            Filter the search regarding the search query
        """
        return query.filter(OperationComptable.company_id==company_id)

    @staticmethod
    def _filter_year(query, year):
        """
            Filter the search on the year
        """
        return query.filter(OperationComptable.year==year)

    @staticmethod
    def _filter_search(query, search):
        """
            Filter the search on the label
        """
        return query.filter(or_(OperationComptable.label.like("%"+search+"%"),
                                OperationComptable.amount==search
                                )
                            )

    @view_config(route_name="operations",
                    renderer="comptability/operation_edit.mako",
                    request_method="POST",
                    permission='manage')
    @view_config(route_name="operation",
                    renderer="comptability/operation_edit.mako",
                    request_param="action=edit",
                    permission='manage')
    def _new_or_edit(self):
        """
            Add a new operation or edit existing one
        """
        if self.request.context.__name__ == "operation":
            edit = True
            operation = self.request.context
            title = u"Édition d'une opération comptable"
            valid_msg = u"L'opération comptable a bien été éditée"
        else:
            edit = False
            operation = OperationComptable()
            title = u"Ajout d'une opération comptable"
            valid_msg = u"L'opération comptable a bien été enregistrée"

        form = self._get_operation_form(edit=edit)
        if 'submit' in self.request.params:
            # form POSTed
            datas = self.request.params.items()
            try:
                app_datas = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                operation = merge_session_with_post(operation, app_datas)
                log.debug(operation.appstruct())
                operation = self.dbsession.merge(operation)
                self.dbsession.flush()
                self.request.session.flash(valid_msg, queue="main")
                return HTTPFound(self.request.route_path('operations'))
        else:
            html_form = form.render(operation.appstruct())
        return dict(title=title,
                    html_form=html_form)

    def _import(self):
        """
            Operations import
        """
        #TODO
        pass

    @view_config(route_name="operation", request_param="action=delete",
                permission='manage')
    def _delete(self):
        """
            Delete a recorded operation
        """
        operation = self.request.context
        self.dbsession.delete(operation)
        self.request.session.flash(u"L'opération a bien été supprimée",
                                                           queue='main')
        return HTTPFound(self.request.route_path('operations'))
