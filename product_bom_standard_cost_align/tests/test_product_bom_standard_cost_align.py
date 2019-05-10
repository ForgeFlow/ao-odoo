# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestProductBomStandardCostAlign(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductBomStandardCostAlign, cls).setUpClass()

        cls.categ_obj = cls.env['product.category']
        cls.product_obj = cls.env['product.product']
        cls.bom_obj = cls.env['mrp.bom']
        cls.bom_line_obj = cls.env['mrp.bom.line']
        cls.production_obj = cls.env['mrp.production']
        cls.wiz_obj = cls.env['stock.change.standard.price']
        cls.produce_wiz = cls.env['mrp.product.produce']
        cls.sm_obj = cls.env['stock.move']

        cls.uom_unit = cls.env.ref('product.product_uom_unit')
        cls.uom_dozen = cls.env.ref('product.product_uom_dozen')
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.customer_location = cls.env.ref('stock.stock_location_customers')

        # Create product category
        categ_standard = cls.categ_obj.create({
            'name': 'Standard cost',
            'property_cost_method': 'standard',
        })
        categ_average = cls.categ_obj.create({
            'name': 'Average cost',
            'property_cost_method': 'average',
        })
        categ_fifo = cls.categ_obj.create({
            'name': 'FIFO cost',
            'property_cost_method': 'fifo',
            'property_valuation': 'real_time',
        })

        # Create products:
        cls.product_1 = cls.product_obj.create({
            'name': 'TEST 01',
            'categ_id': categ_standard.id,
            'type': 'product',
            'standard_price': 300.0,
        })
        cls.product_2 = cls.product_obj.create({
            'name': 'TEST 02',
            'categ_id': categ_average.id,
            'type': 'product',
            'standard_price': 300.0,
        })
        cls.product_3 = cls.product_obj.create({
            'name': 'TEST 03',
            'categ_id': categ_fifo.id,
            'type': 'product',
            'standard_price': 300.0,
        })
        cls.component_1 = cls.product_obj.create({
            'name': 'RM 01',
            'categ_id': categ_standard.id,
            'type': 'product',
            'standard_price': 100.0,
        })
        cls.component_2 = cls.product_obj.create({
            'name': 'RM 01',
            'categ_id': categ_standard.id,
            'type': 'product',
            'standard_price': 75.0,
        })

        # Create Bills of Materials:
        cls.bom_1 = cls.bom_obj.create({
            'product_tmpl_id': cls.product_1.product_tmpl_id.id,

        })
        cls.bom_line_obj.create({
            'product_id': cls.component_1.id,
            'bom_id': cls.bom_1.id,
            'product_qty': 2.0,
        })
        cls.bom_line_obj.create({
            'product_id': cls.component_2.id,
            'bom_id': cls.bom_1.id,
            'product_qty': 5.0,
        })

        cls.bom_2 = cls.bom_obj.create({
            'product_tmpl_id': cls.product_2.product_tmpl_id.id,

        })
        cls.bom_line_obj.create({
            'product_id': cls.component_1.id,
            'bom_id': cls.bom_2.id,
            'product_qty': 2.0,
        })
        cls.bom_line_obj.create({
            'product_id': cls.component_2.id,
            'bom_id': cls.bom_2.id,
            'product_qty': 5.0,
        })

        cls.bom_3 = cls.bom_obj.create({
            'product_tmpl_id': cls.product_3.product_tmpl_id.id,

        })
        cls.bom_line_obj.create({
            'product_id': cls.component_1.id,
            'bom_id': cls.bom_3.id,
            'product_qty': 2.0,
        })
        cls.bom_line_obj.create({
            'product_id': cls.component_2.id,
            'bom_id': cls.bom_3.id,
            'product_qty': 5.0,
        })
        cls.default_fields = ['new_price', 'counterpart_account_id',
                              'counterpart_account_id_required']

    def with_context(self, *args, **kwargs):
        context = dict(args[0] if args else self.env.context, **kwargs)
        self.env = self.env(context=context)
        return self

    def test_01_standard_cost(self):
        self.assertEqual(self.product_1.standard_price, 300.0)
        self.assertEqual(self.product_1.bom_standard_cost, 575.0)
        self.assertTrue(self.product_2.is_cost_misaligned)
        self.wiz_obj = self.wiz_obj.with_context(
            bom_standard_cost=True, active_id=self.product_1.id,
            active_ids=[self.product_1.id],
            active_model='product.product')
        wizard_vals = self.wiz_obj.default_get(self.default_fields)
        wiz = self.wiz_obj.create(wizard_vals)
        wiz.change_price()
        self.assertEqual(self.product_1.standard_price, 575.0)

    def test_02_average(self):
        self.assertEqual(self.product_2.standard_price, 300.0)
        self.assertTrue(self.product_2.is_cost_misaligned)
        self.wiz_obj = self.wiz_obj.with_context(
            bom_standard_cost=True, active_id=self.product_2.id,
            active_ids=[self.product_2.id],
            active_model='product.product')
        wizard_vals = self.wiz_obj.default_get(self.default_fields)
        wiz = self.wiz_obj.create(wizard_vals)
        wiz.change_price()
        self.assertEqual(self.product_2.standard_price, 575.0)

    def test_03_average_valuation(self):
        self.assertEqual(self.product_3.standard_price, 300.0)
        self.assertTrue(self.product_3.is_cost_misaligned)
        self.wiz_obj = self.wiz_obj.with_context(
            bom_standard_cost=True, active_id=self.product_3.id,
            active_ids=[self.product_3.id],
            active_model='product.product')
        wizard_vals = self.wiz_obj.default_get(self.default_fields)
        wiz = self.wiz_obj.create(wizard_vals)
        wiz.change_price()
        self.assertEqual(self.product_3.standard_price, 300.0)
