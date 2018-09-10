# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestCostFinishedProduct(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCostFinishedProduct, cls).setUpClass()

        cls.categ_obj = cls.env['product.category']
        cls.product_obj = cls.env['product.product']
        cls.bom_obj = cls.env['mrp.bom']
        cls.bom_line_obj = cls.env['mrp.bom.line']
        cls.production_obj = cls.env['mrp.production']
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

    def _produce(self, mo, qty=0.0):
        wiz = self.produce_wiz.with_context({
            'active_id': mo.id,
            'active_ids': [mo.id],
        }).create({
            'product_qty': qty or mo.product_qty,
        })
        wiz.do_produce()
        return True

    def test_01_standard_cost(self):
        mo = self.production_obj.create({
            'name': 'MO-01',
            'product_id': self.product_1.id,
            'product_uom_id': self.product_1.uom_id.id,
            'product_qty': 5.0,
            'bom_id': self.bom_1.id,
        })
        mo.action_assign()
        self.assertEqual(self.product_1.standard_price, 300.0)
        self._produce(mo)
        mo.button_mark_done()
        self.assertEqual(mo.move_finished_ids[0].price_unit, 300.0)
        self.assertEqual(self.product_1.standard_price, 300.0)

    def test_02_average_cost(self):
        mo = self.production_obj.create({
            'name': 'MO-02',
            'product_id': self.product_2.id,
            'product_uom_id': self.product_2.uom_id.id,
            'product_qty': 5.0,
            'bom_id': self.bom_2.id,
        })
        mo.action_assign()
        self.assertEqual(self.product_2.standard_price, 300.0)
        self._produce(mo)
        mo.button_mark_done()
        self.assertEqual(mo.move_finished_ids[0].price_unit, 575.0)
        self.assertEqual(self.product_2.standard_price, 575.0)

    def test_03_uom(self):
        """Test if the MO uses a different UoM."""
        mo = self.production_obj.create({
            'name': 'MO-03',
            'product_id': self.product_2.id,
            'product_uom_id': self.uom_dozen.id,
            'product_qty': 1.0,
            'bom_id': self.bom_2.id,
        })
        mo.action_assign()
        self.assertEqual(self.product_2.standard_price, 300.0)
        self._produce(mo)
        mo.button_mark_done()
        self.assertEqual(mo.move_finished_ids[0].price_unit, 575.0)
        self.assertEqual(self.product_2.standard_price, 575.0)

    def test_04_fifo_cost(self):
        mo = self.production_obj.create({
            'name': 'MO-03',
            'product_id': self.product_3.id,
            'product_uom_id': self.product_3.uom_id.id,
            'product_qty': 5.0,
            'bom_id': self.bom_3.id,
        })
        mo.action_assign()
        self.assertEqual(self.product_3.standard_price, 300.0)
        self._produce(mo)
        mo.button_mark_done()
        self.assertEqual(mo.move_finished_ids[0].price_unit, 575.0)
        self.assertEqual(self.product_3.standard_price, 300.0)
        # Create a outgoing move to test valuation:
        out_move = self.sm_obj.create({
            'name': 'test outgoing move',
            'product_id': self.product_3.id,
            'product_uom_qty': 5.0,
            'product_uom': self.product_3.uom_id.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
        })
        out_move._action_confirm()
        out_move._action_assign()
        out_move.move_line_ids[0].qty_done = 5.0
        out_move._action_done()
        self.assertEqual(self.product_3.standard_price, 575.0)

    def test_05_partial_production(self):
        """Cost is correct when producing partial quantities of the MO."""
        mo = self.production_obj.create({
            'name': 'MO-02',
            'product_id': self.product_2.id,
            'product_uom_id': self.product_2.uom_id.id,
            'product_qty': 5.0,
            'bom_id': self.bom_2.id,
        })
        mo.action_assign()
        self.assertEqual(self.product_2.standard_price, 300.0)
        self._produce(mo, 2.0)
        mo.post_inventory()
        self.assertEqual(mo.move_finished_ids[0].price_unit, 575.0)
        self.assertEqual(self.product_2.standard_price, 575.0)
        self._produce(mo, 1.0)
        self._produce(mo, 1.0)
        mo.button_mark_done()
        for m in mo.move_finished_ids:
            self.assertEqual(m.price_unit, 575.0)
        self.assertEqual(self.product_2.standard_price, 575.0)
