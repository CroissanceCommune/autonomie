# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from collections import OrderedDict

from autonomie.export.utils import write_file_to_request
from autonomie.utils.files import get_timestamped_filename

from autonomie.models.expense.payment import ExpensePayment
from autonomie.compute.sage import ExpensePaymentExport
from autonomie.export.sage import SageExpensePaymentCsvWriter
from autonomie.utils import strings
from autonomie.utils.widgets import ViewLink

from autonomie.views.export.utils import (
    get_period_form,
    get_all_form,
    get_expense_id_form,
)

from autonomie.views.export import BaseExportView

logger = logging.getLogger(__name__)


ERR_COMPANY_CONFIG = u"""Un paiement de la feuille de notes de dépense {0}
n'est pas exportable : Des informations sur l'entreprise sont manquantes : {1}
<a onclick="openPopup('{2}');" href='#'>Voir l'entreprise</a>"""
ERR_USER_CONFIG = u"""Un paiement de la feuille de notes de dépense {0}
n'est pas exportable : Des informations sur l'entrepreneur sont manquantes : {1}
<a onclick="openPopup('{2}');" href='#'>Voir l'entrepreneur</a>"""

ERR_BANK_CONFIG = u"""Un paiement de la feuille de notes de dépense {0}
n'est pas exportable : Le paiement n'est associé à aucune banque
<a onclick="openPopup('{1}');" href='#'>Voir le paiement</a>"""
ERR_WAIVER_CONFIG = u"""Le compte pour les abandons de créances n'a pas
été configuré, vous pouvez le configurer
<a onclick="openPopup('{2}');" href='#'>Ici</a>
"""


class SageExpensePaymentExportPage(BaseExportView):
    """
    Provide an expense payment export page
    """
    title = u"Export des règlements de notes de frais au format CSV pour Sage"
    admin_route_name = 'admin_expense_treasury'

    def _populate_action_menu(self):
        self.request.actionmenu.add(
            ViewLink(
                label=u"Liste des notes de dépenses",
                path='expenses',
            )
        )

    def before(self):
        self._populate_action_menu()

    def get_forms(self):
        """
        Implement parent get_forms method
        """
        result = OrderedDict()
        period_form = get_period_form(
            self.request,
            title=u"Exporter les paiements saisis sur la période donnée"
        )
        expense_id_form = get_expense_id_form(
            self.request,
            period_form.counter,
            title=u"Exporter les paiements correspondant à une feuille \
de notes de dépense",
        )
        all_form = get_all_form(
            self.request,
            period_form.counter,
            title=u"Exporter les paiements non exportées",
        )
        for form in period_form, expense_id_form, all_form:
            result[form.formid] = {'form': form, 'title': form.schema.title}
        return result

    def _filter_date(self, query, start_date, end_date):
        return query.filter(
            ExpensePayment.created_at.between(start_date, end_date)
        )

    def _filter_number(self, query, sheet_id):
        return query.filter(ExpensePayment.expense_sheet_id == sheet_id)

    def query(self, query_params_dict, form_name):
        """
            Retrieve the exports we want to export
        """
        query = ExpensePayment.query()

        if form_name == 'period_form':
            start_date = query_params_dict['start_date']
            end_date = query_params_dict['end_date']
            query = self._filter_date(query, start_date, end_date)

        elif form_name == 'expense_id_form':
            sheet_id = query_params_dict['sheet_id']
            query = self._filter_number(query, sheet_id)

        if 'exported' not in query_params_dict or \
                not query_params_dict.get('exported'):
            query = query.filter_by(exported=False)

        return query

    def _check_bank(self, payment):
        if not payment.bank and not payment.waiver:
            return False
        return True

    def _check_company(self, company):
        if not company.code_compta:
            return False
        return True

    def _check_user(self, user):
        if not user.compte_tiers:
            return False
        return True

    def _check_waiver(self, payment):
        """
        Check that the wayver cg account has been configured
        """
        if not self.request.config.get('compte_cg_waiver_ndf'):
            return False
        return True

    def check(self, payments):
        """
        Check that the given expense_payments can be exported

        :param obj payments: A SQLA query of ExpensePayment objects
        """
        count = payments.count()
        if count == 0:
            title = u"Il n'y a aucun paiement à exporter"
            res = {
                'title': title,
                'errors': [],
            }
            return False, res

        title = u"Vous vous apprêtez à exporter {0} paiements".format(
                count)
        res = {'title': title, 'errors': []}

        for payment in payments:
            expense = payment.expense
            company = expense.company
            if not self._check_company(company):
                company_url = self.request.route_path(
                    "company",
                    id=company.id,
                    _query={'action': 'edit'},
                )
                message = ERR_COMPANY_CONFIG.format(
                    expense.id,
                    company.name,
                    company_url,
                )
                res['errors'].append(message)
                continue

            user = expense.user
            if not self._check_user(user):
                user_url = self.request.route_path(
                    "user",
                    id=user.id,
                    _query={'action': 'edit'},
                )
                message = ERR_USER_CONFIG.format(
                    expense.id,
                    strings.format_account(user),
                    user_url,
                )
                res['errors'].append(message)
                continue

            if not self._check_bank(payment):
                payment_url = self.request.route_path(
                    'expensepayment',
                    id=payment.id,
                    _query={'action': 'edit'}
                )
                message = ERR_BANK_CONFIG.format(
                    expense.id,
                    payment_url)
                res['errors'].append(message)
                continue

            if payment.waiver and not self._check_waiver(payment):
                admin_url = self.request.route_path(
                    'admin_expense_treasury'
                )
                message = ERR_WAIVER_CONFIG.format(admin_url)
                res['errors'].append(message)
                continue

        return len(res['errors']) == 0, res

    def record_exported(self, payments, form_name, appstruct):
        """
        Record that those payments have already been exported
        """
        for payment in payments:
            logger.info(
                u"The payment id : {0} (expense {1}) has been exported"
                .format(
                    payment.id,
                    payment.expense.id,
                )
            )
            payment.exported = True
            self.request.dbsession.merge(payment)

    def write_file(self, payments, form_name, appstruct):
        """
        Write the exported csv file to the request
        """
        exporter = ExpensePaymentExport(self.context, self.request)
        writer = SageExpensePaymentCsvWriter()
        writer.set_datas(exporter.get_book_entries(payments))
        write_file_to_request(
            self.request,
            get_timestamped_filename(u"export_paiement_ndf", writer.extension),
            writer.render(),
            headers="application/csv")
        return self.request.response


def add_routes(config):
    config.add_route(
        '/export/treasury/expense_payments',
        '/export/treasury/expense_payments'
    )
    config.add_route(
        '/export/treasury/expense_payments/{id}',
        '/export/treasury/expense_payments/{id}'
    )


def add_views(config):
    config.add_view(
        SageExpensePaymentExportPage,
        route_name='/export/treasury/expense_payments',
        renderer='/export/main.mako',
        permission='admin_treasury',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
