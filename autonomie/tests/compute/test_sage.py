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



class TestSageInvoice(BaseTestCase):
    """
        test Sage Invoice wrapper that group lines by products
    """
    def _prepare(self):
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

        company = Dummy(name="company", code_compta="COMP", compte_cg='COMP_CG')
        client = Dummy(name="client", compte_tiers="CLIENT")
        invoice = TaskCompute()
        invoice.taskDate = datetime.date(2013, 02, 02)
        invoice.client = client
        invoice.company = company
        invoice.officialNumber = "INV_001"
        invoice.lines = [line1, line2, line3]
        invoice.expenses_ht = 10000
        invoice.expenses = 10000

        return ((tva1, tva2), (p1, p2), invoice)

    def test_get_products(self):
        obj = SageInvoice(invoice=MagicMock())
        obj.products['1'] = {'test_key':'test'}
        self.assertTrue(obj.get_product('1', 'dontcare').has_key('test_key'))
        self.assertEqual(len(obj.get_product('2', 'tva_cg_code').keys()), 2)

    def test_populate_invoice_lines(self):
        tvas, products, invoice = self._prepare()
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
        tvas, products, invoice = self._prepare()
        wrapper = SageInvoice(invoice=invoice,
                compte_cgs={'compte_frais_annexes':'FA0001'})
        wrapper.expense_tva_compte_cg = "TVA0001"
        wrapper._populate_expenses()
        wrapper._round_products()
        self.assertEqual(wrapper.products.keys(), ['FA0001'])
        self.assertEqual(wrapper.products['FA0001']['ht'], 20000)
        self.assertEqual(wrapper.products['FA0001']['tva'], 1960)

    def test_SageFacturation_credit_totalht(self):
        tvas, products, invoice = self._prepare()
        config = dict()
        wrapped_invoice = SageInvoice(invoice=invoice,
                    compte_cgs={'compte_frais_annexes':'FA0001'})
        wrapped_invoice.populate()
        book_entry_factory = SageFacturation(config)
        book_entry_factory.set_invoice(wrapped_invoice)
        product = wrapped_invoice.products['P0001']
        line = book_entry_factory.credit_totalht(product)
        self.assertEqual(line, {'date': '20130202',
            'num_facture':'INV_001',
            'libelle': 'company client',
            'compte_cg': 'P0001',
            'num_analytique': 'COMP',
            'code_tva': 'TVA0001',
            'credit': 20000})

    def test_SageFacturation_credit_tva(self):
        tvas, products, invoice = self._prepare()
        config = dict()
        wrapped_invoice = SageInvoice(invoice=invoice,
                    compte_cgs={'compte_frais_annexes':'FA0001'})
        wrapped_invoice.populate()
        book_entry_factory = SageFacturation(config)
        book_entry_factory.set_invoice(wrapped_invoice)
        product = wrapped_invoice.products['P0001']
        line = book_entry_factory.credit_tva(product)
        self.assertEqual(line, {'date': '20130202',
            'num_facture':'INV_001',
            'libelle': 'company client',
            'compte_cg': 'P0001',
            'num_analytique': 'COMP',
            'code_tva': 'TVA0001',
            'credit': 3920})

    def test_SageFacturation_debit_ttc(self):
        tvas, products, invoice = self._prepare()
        config = dict()
        wrapped_invoice = SageInvoice(invoice=invoice,
                    compte_cgs={'compte_frais_annexes':'FA0001'})
        wrapped_invoice.populate()
        book_entry_factory = SageFacturation(config)
        book_entry_factory.set_invoice(wrapped_invoice)
        product = wrapped_invoice.products['P0001']
        line = book_entry_factory.debit_ttc(product)
        self.assertEqual(line, {'date': '20130202',
            'num_facture':'INV_001',
            'libelle': 'company client',
            'compte_cg': 'COMP_CG',
            'num_analytique': 'COMP',
            'compte_tiers': 'CLIENT',
            'debit': 23920,
            'echeance': '20130304'})
