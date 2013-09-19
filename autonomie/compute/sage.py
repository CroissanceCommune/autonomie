# -*- coding: utf-8 -*-
# * File Name : sage.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-09-2013
# * Last Modified :
#
# * Project :
#
"""
    Computing tools for sage import/export
"""
import datetime
import warnings

from autonomie.models.tva import Tva
from autonomie.compute.math_utils import floor
#FIXME : on a pris le compte_cg comme code tva, pas sûr que ce soit ça
#FIXME : L'ordre des écriture importe-t-il ?
#TODO : gérer le cas où on ne retrouve pas le produit ou la tva associé à une
# ligne

def format_sage_date(date_object):
    """
        format date for sage export
    """
    return date_object.strftime("%Y%m%d")


class MissingData(Exception):
    """
        Raised when no data was retrieved from a lazy relationship
        If an element has an attribute that should point to another model, and
        that this model doesn't exist anymore, we raise this exception.
    """
    pass


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

    def __init__(self, invoice, compte_cgs={}):
        self.products = {}
        self.invoice = invoice
        self.compte_cgs = compte_cgs # compte_rrr

    def get_product(self, compte_cg_produit, compte_cg_tva):
        """
            Return the product dict belonging to the key "compte_cg_produit"
        """
        prod = self.products.setdefault(compte_cg_produit, {})
        if prod == {}:
            prod['compte_cg_produit'] = compte_cg_produit
            prod['compte_cg_tva'] = compte_cg_tva
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
                    line.product.tva.compte_cg
                    )
            prod['tva'] = prod.get('tva', 0) + line.tva_amount()
            prod['ht'] = prod.get('ht', 0) + line.total_ht()

    def _populate_discounts(self):
        """
            populate our object with the content of discount lines
        """
        for line in self.invoice.discounts:
            tva = line.get_tva()
            if tva is None:
                raise MissingData(u"No tva found for this discount line")
            prod = self.get_product(
                    self.compte_cgs['compte_rrr'],
                    tva.compte_cg)
            prod['tva'] = prod.get('tva', 0) + line.tva_amount()
            prod['ht'] = prod.get('ht', 0) + line.total_ht()

    def _populate_expenses(self):
        """
            Add the expenses to our object
        """
        if self.invoice.expenses > 0 or self.invoice.expenses_ht > 0:
            if self.expense_tva_compte_cg is None:
                self.expense_tva_compte_cg = Tva.get_default().compte_cg
            prod = self.get_product(
                        self.compte_cgs["compte_frais_annexes"],
                        self.expense_tva_compte_cg
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
        warnings.warn("Missing specs", DeprecationWarning)
        #self._populate_discounts()
        self._populate_expenses()
        self._round_products()



class BaseSageBookEntryFactory(object):
    """
        Base Sage Export module
    """
    static_columns = ('date',
                      'num_facture',
                      'libelle'
                        )
    variable_columns = ('compte_cg', 'num_analytique', 'compte_tiers',
        'code_tva', 'echeance', 'debit', 'credit')

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

    def get_base_entry(self):
        """
            Return an entry with common parameters
        """
        return dict((key, getattr(self, key)) for key in self.static_columns)


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
                self.invoice.company.name,
                self.invoice.client.name,
                )

    @property
    def num_analytique(self):
        """
            Return the analytic number common to all entries in the current
            export module
        """
        return self.invoice.company.code_compta

    def credit_totalht(self, product):
        """
            Return a Credit Total HT entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=product['compte_cg_produit'],
                num_analytique=self.num_analytique,
                code_tva=product['compte_cg_tva'],
                credit=product['ht']
                )
        return entry

    def credit_tva(self, product):
        """
            Return a Credit TVA entry
        """
        entry = self.get_base_entry()
        entry.update(
                compte_cg=product['compte_cg_produit'],
                num_analytique=self.num_analytique,
                code_tva=product['compte_cg_tva'],
                credit=product['tva']
                )
        return entry

    def debit_ttc(self, product):
        """
            Return a debit TTC entry
        """
        entry = self.get_base_entry()
        echeance = self.invoice.taskDate + datetime.timedelta(days=30)
        entry.update(
                compte_cg=self.invoice.company.compte_cg,
                num_analytique=self.num_analytique,
                compte_tiers=self.invoice.client.compte_tiers,
                echeance=format_sage_date(echeance),
                debit=product['ht'] + product['tva']
                )
        return entry

    def yield_entries(self):
        """
            Produce all the entries for the current task
        """
        for product in self.wrapped_invoice.products.values():
            yield self.credit_totalht(product)
            yield self.credit_tva(product)
            yield self.debit_ttc(product)


class SageContribution(BaseSageBookEntryFactory):
    """
        The contribution module
    """
    pass


class SageAssurance(BaseSageBookEntryFactory):
    """
        The assurance module
    """
    pass


class SageCGScop(BaseSageBookEntryFactory):
    """
        The cgscop module
    """
    pass


class SageRGInterne(BaseSageBookEntryFactory):
    """
        The RGINterne module
    """
    pass


class SageRGClient(BaseSageBookEntryFactory):
    """
        The Rg client module
    """
    pass


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
        "sage_rginterne": SageRGInterne,
        "sage_rgclient": SageRGClient,
        }

    def __init__(self, config):
        self.config = config
        self.modules = list(self._default_modules)
        for config_key, module in self._available_modules:
            if self.config.get(config_key) == '1':
                self.modules.append(module(self.config))

    def get_invoice_book_entries(self, invoice):
        """
            Yield the book entries for a given invoice
        """
        # We wrap the invoice with some common computing tools
        wrapped_invoice = SageInvoice(invoice)
        for module in self.modules:
            module.set_invoice(wrapped_invoice)
            for entry in module.yield_entries():
                yield entry

    def get_book_entries(self, invoicelist):
        """
            Return the book entries for a given invoice
        """
        result = []
        for invoice in invoicelist:
            result.append(list(self.get_invoice_book_entries(invoice)))


