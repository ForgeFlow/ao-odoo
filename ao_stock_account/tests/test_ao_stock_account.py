# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

import odoo.tests.common as common
from odoo.exceptions import UserError
from odoo import fields


class TestAoStockAccount(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAoStockAccount, cls).setUpClass()

        cls.product_obj = cls.env['product.product']
        cls.quant_obj = cls.env['stock.quant']

        cls.stock_location = cls.env.ref('stock.stock_location_stock')

        # Create products:
        cls.product_1 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 10.0,
        })
        cls.product_2 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 15.0,
        })

        # Create quants:
        cls.quant_1 = cls.quant_obj.create({
            'product_id': cls.product_1.id,
            'location_id': cls.stock_location.id,
            'quantity': 12.0,
        })
        cls.quant_2 = cls.quant_obj.create({
            'product_id': cls.product_2.id,
            'location_id': cls.stock_location.id,
            'quantity': 16.0,
        })

    def test_01_standard_cost_valuation(self):
        """Test Standard Cost valuation."""
        self.assertEqual(self.quant_1.standard_valuation, 120.0)
        self.assertEqual(self.quant_2.standard_valuation, 240.0)
        # Change qty:
        self.quant_1.sudo().write({'quantity': 15})
        self.assertEqual(self.quant_1.standard_valuation, 150.0)
        # Change standard cost:
        self.product_1.standard_price = 20.0
        self.assertEqual(self.quant_1.standard_valuation, 300.0)

    def test_02_search_last_date_moved(self):
        """Test search method for last_date_moved"""
        with self.assertRaises(UserError):
            self.product_obj.search([
                ('last_date_moved', 'in', ('april', 'november'))])
        with self.assertRaises(UserError):
            self.product_obj.search([
                ('last_date_moved', '>', 2018)])
        yesterday_dt = datetime.today() - timedelta(days=1)
        yesterday = fields.Datetime.to_string(yesterday_dt)
        products_with_moves = self.product_obj.search([
            ('last_date_moved', '>', yesterday)])
        # all moves should have been created today to run CI:
        self.assertTrue(products_with_moves)
