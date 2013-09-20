# -*- coding: utf-8 -*-
# * File Name : test_sage.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 13-09-2013
# * Last Modified :
#
# * Project :
#
import unittest
import datetime
from mock import MagicMock

from autonomie.compute.task import (
        LineCompute,
        TaskCompute,
        InvoiceCompute,
        )
from autonomie.compute.sage import (
        SageInvoice,
        SageFacturation,
        SageContribution,
        SageAssurance,
        SageCGScop,
        SageRGInterne,
        SageRGClient,
        SageExport,
        )

from autonomie.tests.base import BaseTestCase


class Dummy(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class DummyLine(Dummy, LineCompute):
    """
        Dummy line model
    """
    tva_object = None
    def get_tva(self):
        return self.tva_object


class DummyInvoice(Dummy, InvoiceCompute):
    pass

def get_config():
    return {
            'code_journal': 'CODE_JOURNAL',
            'compte_cg_contribution':'CG_CONTRIB',
            'compte_rrr': 'CG_RRR',
            'compte_frais_annexes': 'CG_FA',
            'compte_cg_assurance': 'CG_ASSUR',
            'compte_cg_debiteur': 'CG_DEB',
            'compte_cgscop': 'CG_SCOP',
            'compte_rg_externe': 'CG_RG_EXT',
            'compte_rg_interne': 'CG_RG_INT',
            'numero_analytique': 'NUM_ANA',
            'rg_coop': 'CG_RG_COOP',
            'taux_assurance': "5",
            'taux_cgscop': "5",
            'taux_rg_interne': "5",
            'taux_rg_client': "5",
            'contribution_cae': "10"
            }

def prepare():
    tva1 = MagicMock(name="tva1", value=1960, default=0,
            compte_cg="TVA0001")
    tva2 = MagicMock(name="tva2", value=700, default=0,
            compte_cg="TVA0002")

    p1 = MagicMock(name="product 1", compte_cg="P0001", tva=tva1)
    p2 = MagicMock(name="product 2", compte_cg="P0002", tva=tva2)

    line1 = DummyLine(cost=10000, quantity=1, tva=tva1.value, product=p1,
            tva_object=tva1)
    line2 = DummyLine(cost=10000, quantity=1, tva=tva1.value, product=p1,
            tva_object=tva1)
    line3 = DummyLine(cost=10000, quantity=1, tva=tva2.value, product=p2,
            tva_object=tva2)

    company = Dummy(name="company", code_compta='COMP_CG',
            compte_cg_banque='COMP_BANK_CG', contribution=None)
    client = Dummy(name="client", compte_tiers="CLIENT",
            compte_cg='CG_CLIENT')
    invoice = TaskCompute()
    invoice.taskDate = datetime.date(2013, 02, 02)
    invoice.client = client
    invoice.company = company
    invoice.officialNumber = "INV_001"
    invoice.lines = [line1, line2, line3]
    invoice.expenses_ht = 10000
    invoice.expenses = 10000

    return ((tva1, tva2), (p1, p2), invoice)



class TestSageInvoice(BaseTestCase):
    """
        test Sage Invoice wrapper that group lines by products
    """
    def test_get_products(self):
        obj = SageInvoice(invoice=MagicMock())
        obj.products['1'] = {'test_key':'test'}
        self.assertTrue(obj.get_product('1', 'dontcare').has_key('test_key'))
        self.assertEqual(len(obj.get_product('2', 'tva_cg_code').keys()), 2)

    def test_populate_invoice_lines(self):
        tvas, products, invoice = prepare()
        wrapper = SageInvoice(invoice=invoice)
        wrapper._populate_invoice_lines()
        wrapper._round_products()
        self.assertEqual(wrapper.products.keys(), ['P0001', 'P0002'])
        self.assertEqual(wrapper.products['P0001']['ht'], 20000)
        self.assertEqual(wrapper.products['P0001']['tva'], 3920)
        self.assertEqual(wrapper.products['P0002']['ht'], 10000)
        self.assertEqual(wrapper.products['P0002']['tva'], 700)

    @unittest.skip("This functionnality is not implemented yet, missing specs")
    def test_populate_discount_lines(self):
        pass

    def test_populate_expenses(self):
        tvas, products, invoice = prepare()
        wrapper = SageInvoice(invoice=invoice, compte_cgs=get_config())
        wrapper.expense_tva_compte_cg = "TVA0001"
        wrapper._populate_expenses()
        wrapper._round_products()
        self.assertEqual(wrapper.products.keys(), ['CG_FA'])
        self.assertEqual(wrapper.products['CG_FA']['ht'], 20000)
        self.assertEqual(wrapper.products['CG_FA']['tva'], 1960)

class BaseBookEntryTest(BaseTestCase):
    factory = None

    def _test_product_book_entry(self, method, exp_res, prod_cg='P0001'):
        """
        test a book_entry output (one of a product)
        """
        tvas, products, invoice = prepare()
        config = get_config()
        wrapped_invoice = SageInvoice(invoice=invoice, compte_cgs=config)
        wrapped_invoice.populate()
        book_entry_factory = self.factory(config)
        book_entry_factory.set_invoice(wrapped_invoice)
        product = wrapped_invoice.products[prod_cg]
        line = getattr(book_entry_factory, method)(product)
        exp_res['date'] = '020213'
        exp_res['num_facture'] = 'INV_001'
        exp_res['code_journal'] = 'CODE_JOURNAL'
        self.assertEqual(line, exp_res)

    def _test_invoice_book_entry(self, method, exp_res):
        """
        test a book_entry output (one of a product)
        """
        tvas, products, invoice = prepare()
        config = get_config()
        wrapped_invoice = SageInvoice(invoice=invoice, compte_cgs=config)
        wrapped_invoice.populate()
        book_entry_factory = self.factory(config)
        book_entry_factory.set_invoice(wrapped_invoice)
        line = getattr(book_entry_factory, method)()
        exp_res['date'] = '020213'
        exp_res['num_facture'] = 'INV_001'
        exp_res['code_journal'] = 'CODE_JOURNAL'
        print exp_res
        self.assertEqual(line, exp_res)


class TestSageFacturation(BaseBookEntryTest):
    factory = SageFacturation

    def test_credit_totalht(self):
        res = {'libelle': 'client company',
            'compte_cg': 'P0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'TVA0001',
            'credit': 20000}
        method = "credit_totalht"
        self._test_product_book_entry(method, res)

    def test_credit_tva(self):
        res = {'libelle': 'client company',
            'compte_cg': 'P0001',
            'num_analytique': 'COMP_CG',
            'code_tva': 'TVA0001',
            'credit': 3920}
        method = "credit_tva"
        self._test_product_book_entry(method, res)

    def test_debit_ttc(self):
        method = "debit_ttc"
        res = {'libelle': 'client company',
            'compte_cg': 'COMP_CG',
            'num_analytique': 'COMP_CG',
            'compte_tiers': 'CLIENT',
            'debit': 23920,
            'echeance': '040313'}
        self._test_product_book_entry(method, res)


class TestSageContribution(BaseBookEntryTest):
    factory = SageContribution

    def test_debit_entreprise(self):
        method = "debit_entreprise"
        res = {'libelle': 'client company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'COMP_CG',
            'debit':2000}
        self._test_product_book_entry(method, res)

    def test_credit_entreprise(self):
        method = "credit_entreprise"
        res = {'libelle': 'client company',
            'compte_cg': 'COMP_BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':2000}
        self._test_product_book_entry(method, res)

    def test_debit_cae(self):
        method = "debit_cae"
        res = {'libelle': 'client company',
            'compte_cg': 'COMP_BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':2000}
        self._test_product_book_entry(method, res)

    def test_credit_cae(self):
        method = "credit_cae"
        res = {'libelle': 'client company',
            'compte_cg': 'CG_CONTRIB',
            'num_analytique': 'NUM_ANA',
            'credit':2000}
        self._test_product_book_entry(method, res)


class TestSageAssurance(BaseBookEntryTest):
    # Amount = 2000 0.05 * somme des ht des lignes + expense_ht
    factory = SageAssurance

    def test_debit_entreprise(self):
        method = 'debit_entreprise'
        res = {
                'libelle': 'client company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'COMP_CG',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_entreprise(self):
        method = 'credit_entreprise'
        res = {
                'libelle': 'client company',
                'compte_cg': 'COMP_BANK_CG',
                'num_analytique': 'COMP_CG',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_debit_cae(self):
        method = 'debit_cae'
        res = {
                'libelle': 'client company',
                'compte_cg': 'COMP_BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_cae(self):
        method = 'credit_cae'
        res = {
                'libelle': 'client company',
                'compte_cg': 'CG_ASSUR',
                'num_analytique': 'NUM_ANA',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)


class TestSageCGScop(BaseBookEntryTest):
    factory = SageCGScop

    def test_debit_entreprise(self):
        method = 'debit_entreprise'
        res = {
                'libelle': 'client company',
                'compte_cg': 'CG_SCOP',
                'num_analytique': 'COMP_CG',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_entreprise(self):
        method = 'credit_entreprise'
        res = {
                'libelle': 'client company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'COMP_BANK_CG',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_debit_cae(self):
        method = 'debit_cae'
        res = {
                'libelle': 'client company',
                'compte_cg': 'COMP_BANK_CG',
                'num_analytique': 'NUM_ANA',
                'debit': 2000,
                }
        self._test_invoice_book_entry(method, res)

    def test_credit_cae(self):
        method = 'credit_cae'
        res = {
                'libelle': 'client company',
                'compte_cg': 'CG_DEB',
                'num_analytique': 'NUM_ANA',
                'credit': 2000,
                }
        self._test_invoice_book_entry(method, res)


class TestSageRGInterne(BaseBookEntryTest):
    factory = SageRGInterne

    def test_debit_entreprise(self):
        method = "debit_entreprise"
        res = {'libelle': 'RG COOP client company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'COMP_CG',
            'debit':1196}
        self._test_product_book_entry(method, res)

    def test_credit_entreprise(self):
        method = "credit_entreprise"
        res = {'libelle': 'RG COOP client company',
            'compte_cg': 'COMP_BANK_CG',
            'num_analytique': 'COMP_CG',
            'credit':1196}
        self._test_product_book_entry(method, res)

    def test_debit_cae(self):
        method = "debit_cae"
        res = {'libelle': 'RG COOP client company',
            'compte_cg': 'COMP_BANK_CG',
            'num_analytique': 'NUM_ANA',
            'debit':1196}
        self._test_product_book_entry(method, res)

    def test_credit_cae(self):
        method = "credit_cae"
        res = {'libelle': 'RG COOP client company',
            'compte_cg': 'CG_RG_INT',
            'num_analytique': 'NUM_ANA',
            'credit':1196}
        self._test_product_book_entry(method, res)


class TestSageRGClient(BaseBookEntryTest):
    factory = SageRGClient

    def test_debit_entreprise(self):
        method = 'debit_entreprise'
        res = {
                'libelle': 'RG client company',
                'compte_cg': 'CG_RG_EXT',
                'num_analytique': 'COMP_CG',
                'echeance':'020214',
                'debit': 1196,
                }
        self._test_product_book_entry(method, res)

    def test_credit_entreprise(self):
        method = 'credit_entreprise'
        res = {
                'libelle': 'RG client company',
                'num_analytique': 'COMP_CG',
                'compte_cg': 'CG_CLIENT',
                'compte_tiers': 'CLIENT',
                'echeance':'020214',
                'credit': 1196,
                }
        self._test_product_book_entry(method, res)


class TestSageExport(BaseTestCase):
    def test_modules(self):
        config = {'sage_contribution':'1',
                'sage_assurance':'1',
                'sage_cgscop':'0'}
        exporter = SageExport(config)
        self.assertEqual(len(exporter.modules), 3)
        sage_factories = [SageFacturation, SageContribution, SageAssurance]
        for fact in sage_factories:
            self.assertTrue(True in [isinstance(module, fact)
                for module in exporter.modules])
