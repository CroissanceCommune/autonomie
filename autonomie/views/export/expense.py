# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from collections import OrderedDict
from sqlalchemy import or_

from autonomie.models.expense.sheet import ExpenseSheet
from autonomie.models.expense.types import ExpenseType

from autonomie.export.utils import write_file_to_request
from autonomie.utils.files import get_timestamped_filename
from autonomie.utils import strings
from autonomie.utils.widgets import ViewLink

from autonomie.views.export import BaseExportView
from autonomie.views.export.utils import (
    get_expense_all_form,
    get_expense_id_form,
    get_expense_form,
)


logger = logging.getLogger(__name__)

EXPENSE_CONFIG_ERROR_MSG = u"Veuillez vous assurer que tous les éléments de \
configuration nécessaire à l'export des notes de dépense ont \
bien été fournis : <br /><a href='{0}' target='_blank'>Configuration des \
notes de dépense</a> <br/><a href='{1}' target='_blank'>Configuration \
comptables du module vente</a>"


class SageExpenseExportPage(BaseExportView):
    """
    Sage Expense export views
    """
    title = u"Export des notes de dépense au format CSV pour Sage"
    config_keys = ('compte_cg_ndf', 'code_journal_ndf',)
    contribution_config_keys = (
        'compte_cg_contribution', 'contribution_cae', 'numero_analytique',
    )
    admin_route_name = 'admin_expense'

    def _populate_action_menu(self):
        self.request.actionmenu.add(
            ViewLink(
                label=u"Liste des notes de dépenses",
                path='expenses',
            )
        )

    def before(self):
        self._populate_action_menu()

    def _get_forms(
        self,
        prefix=u'0',
        label=u"dépenses",
        genre=u'e',
        counter=None
    ):
        """
        Generate forms for the given parameters

        :param str prefix: The prefix to give to the form ids
        :param str label: The label of our expense type
        :param str genre: 'e' or ''
        :returns: A dict with forms in it
            {formid: {'form': form, title:formtitle}}
        :rtype: OrderedDict
        """
        result = OrderedDict()

        main_form = get_expense_form(
            self.request,
            title=u"Exporter des %s" % label,
            prefix=prefix,
            counter=counter,
        )
        id_form = get_expense_id_form(
            self.request,
            main_form.counter,
            title=u"Exporter des %s depuis un identifiant" % label,
            prefix=prefix,
        )
        all_form = get_expense_all_form(
            self.request,
            main_form.counter,
            title=u"Exporter les %s non exporté%ss" % (label, genre),
            prefix=prefix,
        )

        for form in main_form, id_form, all_form:
            result[form.formid] = {'form': form, 'title': form.schema.title}

        return result

    def get_forms(self):
        """
        Implement parent get_forms method
        """
        result = self._get_forms()
        counter = result.values[0].counter
        result.update(
            self._get_forms(
                prefix=u'1', label=u'frais', genre='', counter=counter
            )
        )
        result.update(
            self._get_forms(
                prefix=u'2', label=u'achats', genre='', counter=counter
            )
        )
        return result

    def _filter_by_sheet_id(self, query, appstruct):
        """
        Add an id filter on the query
        :param obj query: A sqlalchemy query
        :param dict appstruct: The form datas
        """
        sheet_id = appstruct['sheet_id']
        return query.filter(ExpenseSheet.id == sheet_id)

    def _filter_by_period(self, query, appstruct):
        """
        Add a filter on month and year
        :param obj query: A sqlalchemy query
        :param dict appstruct: The form datas
        """
        year = appstruct['year']
        query = query.filter(ExpenseSheet.year == year)
        month = appstruct['month']
        query = query.filter(ExpenseSheet.month == month)
        return query

    def _filter_by_user(self, query, appstruct):
        """
        Add a filter on the user_id
        :param obj query: A sqlalchemy query
        :param dict appstruct: The form datas
        """
        if appstruct.get('user_id', 0) != 0:
            user_id = appstruct['user_id']
            query = query.filter(ExpenseSheet.user_id == user_id)
        return query

    def _filter_by_exported(self, query, appstruct):
        """
        Filter exported regarding the category of expense we want to export
        :param obj query: A sqlalchemy query
        :param dict appstruct: The form datas
        """
        if not appstruct.get('exported'):
            export_category = appstruct['category']
            if export_category == '0':
                query = query.filter(
                    or_(
                        ExpenseSheet.purchase_exported == False,
                        ExpenseSheet.expense_exported == False,
                    )
                )

            elif export_category == '1':
                query = query.filter_by(expense_exported=False)

            elif export_category == '2':
                query = query.filter_by(purchase_exported=False)
        return query

    def query(self, appstruct, form_name):
        """
        Base Query for expenses
        :param appstruct: params passed in the query for expense export
        :param str form_name: The submitted form's name
        """
        query = ExpenseSheet.query()
        query = query.filter(ExpenseSheet.status == 'valid')

        if form_name.endswith('_id_form'):
            query = self._filter_by_sheet_id(query, appstruct)

        elif form_name.endswith('_main_form'):
            query = self._filter_by_period(query, appstruct)
            query = self._filter_by_user(query, appstruct)

        query = self._filter_by_exported(query, appstruct)
        return query

    def check_config(self, config):
        """
        Check all configuration values are set for export

        :param config: The application configuration dict
        """
        contribution_is_active = False
        for type_ in ExpenseType.query().filter_by(active=True):
            if not type_.code:  # or not type_.compte_tva or not type_.code_tva:
                return False
            if type_.contribution:
                contribution_is_active = True

        for key in self.config_keys:
            if not config.get(key):
                return False
            if contribution_is_active:
                for key in self.contribution_config_keys:
                    if not config.get(key):
                        return False
        return True

    def check_company(self, company):
        """
        Check if the company is fully configured

        :param company: The company we are exporting expenses from
        """
        if not company.code_compta:
            company_url = self.request.route_path(
                'company',
                id=company.id,
                _query={'action': 'edit'},
            )
            message = u""" Des informations sur l'entreprise {0}
sont manquantes <a href='{1}' target='_blank'>Voir l'entreprise</a>"""
            message = message.format(
                company.name,
                company_url)
            return message
        return None

    def check(self, expenses):
        """
        Check if we can export the expenses

        :param expenses: the expenses to export
        :returns: a 2-uple (is_ok, messages)
        """
        count = expenses.count()
        if count == 0:
            title = u"Il n'y a aucune note de dépense à exporter"
            res = {
                'title': title,
                'errors': []
            }
            return False, res

        title = u"Vous vous apprêtez à exporter {0} notes de dépense".format(
                count)

        errors = []

        if not self.check_config(self.request.config):
            url1 = self.request.route_path('admin_expense')
            url2 = self.request.route_path('admin_vente')
            errors.append(EXPENSE_CONFIG_ERROR_MSG.format(url1, url2))

        for expense in expenses:
            company = expense.company
            error = self.check_company(company)
            if error is not None:
                errors.append(
                    u"La note de dépense de {0} n'est pas exportable "
                    u"<br />{1}".format(
                        strings.format_account(expense.user),
                        error
                    )
                )

        res = {'title': title, 'errors': errors}
        return len(errors) == 0, res

    def record_exported(self, expenses, form_name, appstruct):
        """
        Tag the exported expenses

        :param expenses: The expenses we are exporting
        """
        category = appstruct['category']

        for expense in expenses:
            logger.info(u"The expense with id {0} has been exported".format(
                expense.id))

            if category == '0':
                expense.expense_exported = True
                expense.purchase_exported = True
            elif category == '1':
                expense.expense_exported = True
            elif category == '2':
                expense.purchase_exported = True

            self.request.dbsession.merge(expense)

    def _collect_export_datas(self, expenses, appstruct):
        """
        Collect the datas to export

        If we export all datas, ensure only the non-already exported datas are
        included

        :returns: A list of book entry lines in dict format
        :rtype: list
        """
        force = appstruct.get('exported', False)
        category = appstruct['category']

        from autonomie.interfaces import ITreasuryExpenseProducer
        exporter = self.request.find_service(ITreasuryExpenseProducer)
        datas = []
        if category in ('1', '2') or force:
            datas = exporter.get_book_entries(expenses, category)
        else:
            # If we're not forcing and we export all, we filter regarding which
            # datas were already exported
            for expense in expenses:
                if not expense.expense_exported:
                    datas.extend(exporter.get_book_entry(expense, '1'))

                if not expense.purchase_exported:
                    datas.extend(exporter.get_book_entry(expense, '2'))
        return datas

    def write_file(self, expenses, form_name, appstruct):
        from autonomie.interfaces import ITreasuryExpenseWriter
        writer = self.request.find_service(ITreasuryExpenseWriter)

        datas = self._collect_export_datas(expenses, appstruct)
        writer.set_datas(datas)
        write_file_to_request(
            self.request,
            get_timestamped_filename(u"export_ndf", writer.extension),
            writer.render(),
            headers="application/csv",
        )
        return self.request.response


def add_routes(config):
    config.add_route('/export/treasury/expenses', '/export/treasury/expenses')
    config.add_route(
        '/export/treasury/expenses/{id}',
        '/export/treasury/expenses/{id}'
    )


def add_views(config):
    config.add_view(
        SageExpenseExportPage,
        route_name='/export/treasury/expenses',
        renderer='/export/main.mako',
        permission='admin_treasury',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
