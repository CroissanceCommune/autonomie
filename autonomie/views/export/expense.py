# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from collections import OrderedDict

from autonomie.models.expense.sheet import ExpenseSheet
from autonomie.models.expense.types import ExpenseType

from autonomie.export.utils import write_file_to_request
from autonomie.utils.files import get_timestamped_filename
from autonomie.utils import strings
from autonomie.utils.widgets import ViewLink

from autonomie.views.export import BaseExportView
from autonomie.views.export.utils import (
    get_all_form,
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
        prefix=u'expense',
        label=u"dépenses",
        genre=u'e'
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
        )
        id_form = get_expense_id_form(
            self.request,
            main_form.counter,
            title=u"Exporter des %s depuis un identifiant" % label,
            prefix=prefix,
        )
        all_form = get_all_form(
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
        result.update(
            self._get_forms(prefix=u'frais', label=u'frais', genre='')
        )
        result.update(
            self._get_forms(prefix=u'achats', label=u'achats', genre='')
        )
        return result

    def query(self, query_params_dict, form_name):
        """
        Base Query for expenses
        :param query_params_dict: params passed in the query for expense export
        """
        query = ExpenseSheet.query()
        query = query.filter(ExpenseSheet.status == 'valid')

        if form_name.endswith('id_form'):
            sheet_id = query_params_dict['sheet_id']
            query = query.filter(ExpenseSheet.id == sheet_id)

        elif form_name.endswith('main_form'):
            year = query_params_dict['year']
            query = query.filter(ExpenseSheet.year == year)

            month = query_params_dict['month']
            query = query.filter(ExpenseSheet.month == month)

            if query_params_dict.get('user_id', 0) != 0:
                user_id = query_params_dict['user_id']
                query = query.filter(ExpenseSheet.user_id == user_id)

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter_by(exported=False)

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

    def record_exported(self, expenses):
        """
        Tag the exported expenses

        :param expenses: The expenses we are exporting
        """
        for expense in expenses:
            logger.info(u"The expense with id {0} has been exported".format(
                expense.id))
            expense.exported = True
            self.request.dbsession.merge(expense)

    def write_file(self, expenses):
        """
        """
        from autonomie.interfaces import ITreasuryExpenseProducer
        exporter = self.request.find_service(ITreasuryExpenseProducer)

        from autonomie.interfaces import ITreasuryExpenseWriter
        writer = self.request.find_service(ITreasuryExpenseWriter)

        writer.set_datas(exporter.get_book_entries(expenses))
        write_file_to_request(
            self.request,
            get_timestamped_filename(u"export_ndf", writer.extension),
            writer.render(),
            headers="application/csv")
        self.record_exported(expenses)
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
