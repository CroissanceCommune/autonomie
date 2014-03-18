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
    Computing tools for sage import/export
"""
import datetime
import warnings

from autonomie.models.tva import Tva
from autonomie.compute.math_utils import (
        floor,
        percentage,
        )

def format_sage_date(date_object):
    """
        format date for sage export
    """
    return date_object.strftime("%d%m%y")


class MissingData(Exception):
    """
        Raised when no data was retrieved from a lazy relationship
        If an element has an attribute that should point to another model, and
        that this model doesn't exist anymore, we raise this exception.
    """
    pass

def double_lines(method):
    """
        Wrap a book entry generator by duplicating the analytic book entry as a
        general one
    """
    def wrapped_method(self, *args):
        analytic_entry = method(self, *args)
        general_entry = analytic_entry.copy()
        general_entry['type_'] = 'G'
        general_entry.pop('num_analytique')
        return general_entry, analytic_entry
    return wrapped_method


class SageInvoice(object):
    """
        Sage wrapper for invoices
        1- Peupler les produits
            * Un produit doit avoir:
                * TVA
                * HT
                * Compte CG Produit
                * Compte CG TVA
                * (Code TVA)

        Pour chaque ligne :
            créer produit ou ajouter au produit existant

        Pour chaque ligne de remise:
            créer produit ou ajouter au produit existant

        Si frais HT ou frais TTC:
            créer produit
    """
    expense_tva_compte_cg = None
    expense_tva_code = None

    def __init__(self, invoice, config=None):
        self.products = {}
        self.invoice = invoice
        self.config = config or {}

    def get_product(self, compte_cg_produit, compte_cg_tva, code_tva):
        """
            Return the product dict belonging to the key "compte_cg_produit"
        """
        prod = self.products.setdefault(compte_cg_produit, {})
        if prod == {}:
            prod['compte_cg_produit'] = compte_cg_produit
            prod['compte_cg_tva'] = compte_cg_tva
            prod['code_tva'] = code_tva
        return prod

    def _populate_invoice_lines(self):
        """
            populate the object with the content of our lines
        """
        for line in self.invoice.lines:
            product_model = line.product
            if product_model is None:
                raise MissingData(u"No product found for this invoice line")
            prod = self.get_product(
                    line.product.compte_cg,
                    line.product.tva.compte_cg,
                    line.product.tva.code,
                    )
            prod['tva'] = prod.get('tva', 0) + line.tva_amount()
            prod['ht'] = prod.get('ht', 0) + line.total_ht()

    def _populate_discounts(self):
        """
            populate our object with the content of discount lines
            discount lines are grouped in a unique book entry, the TVA used is
            specific to the RRR, no book entry is returned if the code and
            compte cg for this specific book entry type is defined
        """
        compte_cg_tva = self.config.get('compte_cg_tva_rrr')
        code_tva = self.config.get('code_tva_rrr')
        if compte_cg_tva and code_tva:
            for line in self.invoice.discounts:
                prod = self.get_product(
                        self.config.get('compte_rrr'),
                        compte_cg_tva,
                        code_tva,
                        )
                prod['tva'] = prod.get('tva', 0) + line.tva_amount()
                prod['ht'] = prod.get('ht', 0) + line.total_ht()

    def _populate_expenses(self):
        """
            Add the expenses to our object
        """
        if self.invoice.expenses > 0 or self.invoice.expenses_ht > 0:
            if self.expense_tva_compte_cg is None:
                self.expense_tva_compte_cg = Tva.get_default().compte_cg
                self.expense_tva_code = Tva.get_default().code

            prod = self.get_product(
                        self.config.get("compte_frais_annexes"),
                        self.expense_tva_compte_cg,
                        self.expense_tva_code
                        )
            ht_expense = self.invoice.get_expense_ht()
            ttc_expense = self.invoice.expenses_amount()
            prod['tva'] = ht_expense.tva_amount()
            prod['ht'] = ttc_expense + ht_expense.total_ht()

    def _round_products(self):
        """
            Round the products ht and tva
        """
        for value in self.products.values():
            value['ht'] = floor(value['ht'])
            value['tva'] = floor(value['tva'])

    def populate(self):
        """
            populate the products entries with the current invoice
        """
        self._populate_invoice_lines()
        #warnings.warn("Missing specs", DeprecationWarning)
        self._populate_discounts()
        self._populate_expenses()
        self._round_products()



class BaseSageBookEntryFactory(object):
    """
        Base Sage Export module
    """
    static_columns = (
                      'code_journal',
                      'date',
                      'num_facture',
                      'libelle',
                      'type_',
                        )
    variable_columns = ('compte_cg', 'num_analytique', 'compte_tiers',
        'code_tva', 'echeance', 'debit', 'credit')
    _part_key = ''
    _amount_method = lambda self, a,b: percentage(a,b)

    def __init__(self, config):
        self.config = config
        self.wrapped_invoice = None
        self.invoice = None

    def set_invoice(self, wrapped_invoice):
        """
            Set the current invoice to process
        """
        self.wrapped_invoice = wrapped_invoice
        self.invoice = wrapped_invoice.invoice

    @property
    def code_journal(self):
        """
            Return the code of the destination journal from the treasury book
        """
        return self.config['code_journal']

    @property
    def date(self):
        """
            Return the date field
        """
        return format_sage_date(self.invoice.taskDate)

    @property
    def num_facture(self):
        """
            Return the invoice number
        """
        return self.invoice.officialNumber

    @property
    def libelle(self):
        """
            Return the label for our book entry
            Should be overriden by subclasses
        """
        return ""

    @property
    def type_(self):
        """
            Return A for 'Analytic' book entry
        """
        return "A"

    def get_base_entry(self):
        """
            Return an entry with common parameters
        """
        return dict((key, getattr(self, key)) for key in self.static_columns)

    def get_part(self):
        """
            Return the value used as percentage for the computing the amount
            of a book entry
        """
        try:
            part = float(self.config[self._part_key])
        except ValueError:
            raise MissingData(u"The Taux {0} should be a float"\
                    .format(self._part_key))
        return part


class SageFacturation(BaseSageBookEntryFactory):
    """
        Facturation treasury export module

        For each product exports exportsthree types of treasury lines
            * Crédit TotalHT
            * Crédit TVA
            * Débit TTC

        Expenses and discounts are also exported

        Uses :
            Numéro analytique de l'entreprise
            Compte CG produit
            Compte CG TVA
            Compte CG de l'entreprise
            Compte Tiers du client
            Code TVA

            Compte CG Annexe
            Compte CG RRR

        Columns :
            * Num facture
            * Date
            * Compte CG
            * Numéro analytique
            * Compte Tiers
            * Code TVA
            * Date d'échéance
            * Libellés
            * Montant
    """

    @property
    def libelle(self):
        """
            Return the value of the libelle column
        """
        return u"{0} {1}".format(
                self.invoice.customer.name,
                self.invoice.company.name,
                )

    @property
    def num_analytique(self):
        """
            Return the analytic number common to all entries in the current
            export module
        """
        return self.invoice.company.code_compta

    @double_lines
    def credit_totalht(self, product):
        """
            Return a Credit Total HT entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=product['compte_cg_produit'],
                num_analytique=self.num_analytique,
                code_tva=product['code_tva'],
                credit=product['ht']
                )
        return entry

    @double_lines
    def credit_tva(self, product):
        """
            Return a Credit TVA entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=product['compte_cg_tva'],
                num_analytique=self.num_analytique,
                code_tva=product['code_tva'],
                credit=product['tva']
                )
        return entry

    @double_lines
    def debit_ttc(self, product):
        """
            Return a debit TTC entry
        """
        entry = self.get_base_entry()
        echeance = self.invoice.taskDate + datetime.timedelta(days=30)
        entry.update(
                compte_cg=self.invoice.customer.compte_cg,
                num_analytique=self.num_analytique,
                compte_tiers=self.invoice.customer.compte_tiers,
                echeance=format_sage_date(echeance),
                debit=product['ht'] + product['tva']
                )
        return entry

    @staticmethod
    def _has_tva_value(product):
        """
            Test whether the tva of the given product has a positive value
        """
        return product['tva'] != 0


    def yield_entries(self):
        """
            Produce all the entries for the current task
        """
        for product in self.wrapped_invoice.products.values():
            yield self.credit_totalht(product)
            if self._has_tva_value(product):
                yield self.credit_tva(product)
            yield self.debit_ttc(product)


class SageContribution(BaseSageBookEntryFactory):
    """
        The contribution module
    """
    _part_key = "contribution_cae"
    @property
    def libelle(self):
        return u"{0} {1}".format(
                self.invoice.customer.name,
                self.invoice.company.name,
                )

    def get_contribution(self):
        """
            Return the contribution for the current invoice, the company's one
            or the cae's one by default
        """
        contrib = self.invoice.company.contribution
        if contrib is None:
            contrib = self.get_part()
        return contrib

    def get_amount(self, product):
        """
            Return the amount for the current module
            (the same for credit or debit)
        """
        return percentage(product['ht'], self.get_contribution())

    @double_lines
    def debit_entreprise(self, product):
        """
            Debit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_contribution'],
                num_analytique=self.invoice.company.code_compta,
                debit=self.get_amount(product)
                )
        return entry

    @double_lines
    def credit_entreprise(self, product):
        """
            Credit Entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.invoice.company.code_compta,
                credit=self.get_amount(product)
                )
        return entry

    @double_lines
    def debit_cae(self, product):
        """
            Debit CAE book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.config['numero_analytique'],
                debit=self.get_amount(product))
        return entry

    @double_lines
    def credit_cae(self, product):
        """
            Credit CAE book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_contribution'],
                num_analytique=self.config['numero_analytique'],
                credit=self.get_amount(product))
        return entry

    def yield_entries(self):
        """
            yield book entries
        """
        for product in self.wrapped_invoice.products.values():
            yield self.debit_entreprise(product)
            yield self.credit_entreprise(product)
            yield self.debit_cae(product)
            yield self.credit_cae(product)


class SageAssurance(BaseSageBookEntryFactory):
    """
        The assurance module
    """
    _part_key = 'taux_assurance'
    @property
    def libelle(self):
        return u"{0} {1}".format(
                self.invoice.customer.name,
                self.invoice.company.name,
                )

    def get_amount(self):
        """
            Return the amount for the current module
            (the same for credit or debit)
        """
        return self._amount_method(self.invoice.total_ht(), self.get_part())

    @double_lines
    def debit_entreprise(self):
        """
            Debit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_assurance'],
                num_analytique=self.invoice.company.code_compta,
                debit=self.get_amount(),
                )
        return entry

    @double_lines
    def credit_entreprise(self):
        """
            Credit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.invoice.company.code_compta,
                credit=self.get_amount(),)
        return entry

    @double_lines
    def debit_cae(self):
        """
            Debit cae book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.config['numero_analytique'],
                debit=self.get_amount(),)
        return entry

    @double_lines
    def credit_cae(self):
        """
            Credit CAE book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_assurance'],
                num_analytique=self.config['numero_analytique'],
                credit=self.get_amount(),)
        return entry

    def yield_entries(self):
        """
            yield book entries
        """
        yield self.debit_entreprise()
        yield self.credit_entreprise()
        yield self.debit_cae()
        yield self.credit_cae()



class SageCGScop(BaseSageBookEntryFactory):
    """
        The cgscop module
    """
    _part_key = "taux_cgscop"
    @property
    def libelle(self):
        return u"{0} {1}".format(
                self.invoice.customer.name,
                self.invoice.company.name,
                )

    def get_amount(self):
        """
            Return the amount for the current module
            (the same for credit or debit)
        """
        return self._amount_method(self.invoice.total_ht(), self.get_part())

    @double_lines
    def debit_entreprise(self):
        """
            Debit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cgscop'],
                num_analytique=self.invoice.company.code_compta,
                debit=self.get_amount(),
                )
        return entry

    @double_lines
    def credit_entreprise(self):
        """
            Credit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.invoice.company.code_compta,
                credit=self.get_amount(),)
        return entry

    @double_lines
    def debit_cae(self):
        """
            Debit cae book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.config['numero_analytique'],
                debit=self.get_amount(),)
        return entry

    @double_lines
    def credit_cae(self):
        """
            Credit CAE book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_debiteur'],
                num_analytique=self.config['numero_analytique'],
                credit=self.get_amount(),)
        return entry

    def yield_entries(self):
        """
            yield book entries
        """
        yield self.debit_entreprise()
        yield self.credit_entreprise()
        yield self.debit_cae()
        yield self.credit_cae()


class SageContributionOrganic(BaseSageBookEntryFactory):
    """
        The Organic contribution is due for CAE with a large CA
    """
    _part_key = "taux_contribution_organic"
    @property
    def libelle(self):
        return u"Contribution Organic {0} {1}".format(
                self.invoice.customer.name,
                self.invoice.company.name,
                )

    def get_contribution(self):
        return self.get_part()

    def get_amount(self):
        """
            Return the amount for the current module
            (the same for credit or debit)
        """
        return self._amount_method(self.invoice.total_ht(), self.get_part())

    @double_lines
    def debit_entreprise(self):
        """
            Debit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_organic'],
                num_analytique=self.invoice.company.code_compta,
                debit=self.get_amount(),
                )
        return entry

    @double_lines
    def credit_entreprise(self):
        """
            Credit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.invoice.company.code_compta,
                credit=self.get_amount(),)
        return entry

    @double_lines
    def debit_cae(self):
        """
            Debit cae book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.config['numero_analytique'],
                debit=self.get_amount(),)
        return entry

    @double_lines
    def credit_cae(self):
        """
            Credit CAE book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_debiteur_organic'],
                num_analytique=self.config['numero_analytique'],
                credit=self.get_amount(),)
        return entry

    def yield_entries(self):
        """
            yield book entries
        """
        yield self.debit_entreprise()
        yield self.credit_entreprise()
        yield self.debit_cae()
        yield self.credit_cae()


class SageRGInterne(BaseSageBookEntryFactory):
    """
        The RGINterne module
    """
    _part_key = "taux_rg_interne"
    @property
    def libelle(self):
        return u"RG COOP {0} {1}".format(
                self.invoice.customer.name,
                self.invoice.company.name,
                )

    def get_amount(self, product):
        """
            Return the amount for the current module
            (the same for credit or debit)
        """
        ttc = product['ht'] + product['tva']
        return self._amount_method(ttc, self.get_part())

    @double_lines
    def debit_entreprise(self, product):
        """
            Debit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_rg_interne'],
                num_analytique=self.invoice.company.code_compta,
                debit=self.get_amount(product),
                )
        return entry

    @double_lines
    def credit_entreprise(self, product):
        """
            Credit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.invoice.company.code_compta,
                credit=self.get_amount(product),)
        return entry

    @double_lines
    def debit_cae(self, product):
        """
            Debit cae book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_cg_banque'],
                num_analytique=self.config['numero_analytique'],
                debit=self.get_amount(product),)
        return entry

    @double_lines
    def credit_cae(self, product):
        """
            Credit CAE book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_rg_interne'],
                num_analytique=self.config['numero_analytique'],
                credit=self.get_amount(product),)
        return entry

    def yield_entries(self):
        """
            yield book entries
        """
        for product in self.wrapped_invoice.products.values():
            yield self.debit_entreprise(product)
            yield self.credit_entreprise(product)
            yield self.debit_cae(product)
            yield self.credit_cae(product)


class SageRGClient(BaseSageBookEntryFactory):
    """
        The Rg client module
    """
    _part_key = "taux_rg_client"
    @property
    def libelle(self):
        return u"RG {0} {1}".format(
                self.invoice.customer.name,
                self.invoice.company.name,
                )

    def get_amount(self, product):
        """
            Return the amount for the current module
            (the same for credit or debit)
        """
        ttc = product['ht'] + product['tva']
        return self._amount_method(ttc, self.get_part())

    def get_echeance(self):
        """
            Return the value for the "echeance" column now + 365 days
        """
        echeance = self.invoice.taskDate + datetime.timedelta(days=365)
        return format_sage_date(echeance)

    @double_lines
    def debit_entreprise(self, product):
        """
            Debit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.config['compte_rg_externe'],
                num_analytique=self.invoice.company.code_compta,
                debit=self.get_amount(product),
                echeance=self.get_echeance(),
                )
        return entry

    @double_lines
    def credit_entreprise(self, product):
        """
            Credit entreprise book entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=self.invoice.customer.compte_cg,
                num_analytique=self.invoice.company.code_compta,
                credit=self.get_amount(product),
                compte_tiers=self.invoice.customer.compte_tiers,
                echeance=self.get_echeance(),
                )
        return entry

    def yield_entries(self):
        """
            yield book entries
        """
        for product in self.wrapped_invoice.products.values():
            yield self.debit_entreprise(product)
            yield self.credit_entreprise(product)





class SageExport(object):
    """
        base module for treasury export
        @param config: application configuration dict, contains all the CAE wide
        account configurations
    """
    _default_modules = (SageFacturation,)
    _available_modules = {
        "sage_contribution": SageContribution,
        "sage_assurance": SageAssurance,
        "sage_cgscop": SageCGScop,
        "sage_organic": SageContributionOrganic,
        "sage_rginterne": SageRGInterne,
        "sage_rgclient": SageRGClient,
        }

    def __init__(self, config):
        self.config = config
        self.modules = []
        for module in self._default_modules:
            self.modules.append(module(self.config))
        for config_key, module in self._available_modules.items():
            if self.config.get(config_key) == '1':
                self.modules.append(module(self.config))

    def get_invoice_book_entries(self, invoice):
        """
            Yield the book entries for a given invoice
        """
        # We wrap the invoice with some common computing tools
        wrapped_invoice = SageInvoice(invoice, self.config)
        wrapped_invoice.populate()
        for module in self.modules:
            module.set_invoice(wrapped_invoice)
            for entry in module.yield_entries():
                gen_line, analytic_line = entry
                yield gen_line
                yield analytic_line

    def get_book_entries(self, invoicelist):
        """
            Return the book entries for a given invoice
        """
        result = []
        for invoice in invoicelist:
            result.extend(list(self.get_invoice_book_entries(invoice)))
        return result
