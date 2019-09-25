# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestBomStandardCost(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestBomStandardCost, cls).setUpClass()

        cls.product_obj = cls.env['product.product']
        cls.product_categ_obj = cls.env['product.category']
        cls.account_obj = cls.env['account.account']
        cls.account_move_line_obj = cls.env['account.move.line']
        cls.bom_obj = cls.env['mrp.bom']
        cls.bom_line_obj = cls.env['mrp.bom.line']
        cls.location_production = cls.env.ref('stock.location_production')
        cls.production_obj = cls.env['mrp.production']
        cls.produce_wiz = cls.env['mrp.product.produce']
        cls.unbuild_obj = cls.env['mrp.unbuild']

        # Create accounts for labor, overhead and WIP
        cls.account_labor = cls.env['account.account'].create({
            'name': 'Labor',
            'code': '101180',
            'user_type_id': cls.env.ref(
                'account.data_account_type_current_assets').id
        })
        cls.account_overhead = cls.env['account.account'].create({
            'name': 'Overhead',
            'code': '101190',
            'user_type_id': cls.env.ref(
                'account.data_account_type_current_assets').id
        })
        cls.account_wip = cls.env['account.account'].create({
            'name': 'WIP',
            'code': '999',
            'user_type_id': cls.env.ref(
                'account.data_account_type_current_assets').id
        })

        # Create categories for labor and overhead
        cls.categ_labor = cls.product_categ_obj.create({
            'name': 'Test Labor Category 1',
            'property_labor_account_id': cls.account_labor.id,
        })
        cls.categ_overhead = cls.product_categ_obj.create({
            'name': 'Test Overhead Category 1',
            'property_overhead_account_id': cls.account_overhead.id,
        })
        cls.categ_physical = cls.env.ref('product.product_category_5')
        cls.categ_physical.write({
            'property_valuation': 'real_time',
        })

        # Assign WIP account to stock location production
        cls.location_production.write({
            'valuation_in_account_id': cls.account_wip.id,
            'valuation_out_account_id': cls.account_wip.id,
        })

        # Create products:
        cls.product_top = cls.product_obj.create({
            'name': 'Final Product',
            'type': 'product',
            'categ_id': cls.categ_physical.id,
        })
        cls.product_sub_1 = cls.product_obj.create({
            'name': 'L01-01',
            'type': 'product',
            'standard_price': 100.0,
            'categ_id': cls.categ_physical.id,
        })
        cls.component_1 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 10.0,
            'categ_id': cls.categ_physical.id,
        })
        cls.component_2 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 15.0,
            'categ_id': cls.categ_physical.id,
        })
        cls.component_3 = cls.product_obj.create({
            'name': 'RM 03',
            'type': 'product',
            'standard_price': 20.0,
            'categ_id': cls.categ_physical.id,
        })
        cls.labor_1 = cls.product_obj.create({
            'name': 'Labor 01',
            'type': 'service',
            'standard_price': 25.0,
            'categ_id': cls.categ_labor.id,
        })
        cls.overhead_1 = cls.product_obj.create({
            'name': 'Labor 01',
            'type': 'service',
            'standard_price': 35.0,
            'categ_id': cls.categ_overhead.id,
        })

        # Create Bills of Materials:
        cls.bom_top = cls.bom_obj.create({
            'product_tmpl_id': cls.product_top.product_tmpl_id.id,
            'bom_cost_ids': [
                (0, 0, {
                    'cost_type': 'labor',
                    'product_id': cls.labor_1.id,
                    'product_uom_id': cls.labor_1.uom_id.id,
                    'product_qty': 2.0,
                }), (0, 0, {
                    'cost_type': 'overhead',
                    'product_id': cls.overhead_1.id,
                    'product_uom_id': cls.overhead_1.uom_id.id,
                    'product_qty': 1.0,
                })
            ]
        })
        cls.line_top_1 = cls.bom_line_obj.create({
            'product_id': cls.product_sub_1.id,
            'bom_id': cls.bom_top.id,
            'product_qty': 2.0,
        })
        cls.line_top_2 = cls.bom_line_obj.create({
            'product_id': cls.component_3.id,
            'bom_id': cls.bom_top.id,
            'product_qty': 3.0,
        })

        cls.bom_sub_1 = cls.bom_obj.create({
            'product_tmpl_id': cls.product_sub_1.product_tmpl_id.id,
            'bom_cost_ids': [
                (0, 0, {
                    'cost_type': 'labor',
                    'product_id': cls.labor_1.id,
                    'product_uom_id': cls.labor_1.uom_id.id,
                    'product_qty': 1.0,
                }), (0, 0, {
                    'cost_type': 'overhead',
                    'product_id': cls.overhead_1.id,
                    'product_uom_id': cls.overhead_1.uom_id.id,
                    'product_qty': 2.0,
                })
            ]
        })
        cls.line_sub_1_1 = cls.bom_line_obj.create({
            'product_id': cls.component_1.id,
            'bom_id': cls.bom_sub_1.id,
            'product_qty': 4.0,
        })
        cls.line_sub_1_2 = cls.bom_line_obj.create({
            'product_id': cls.component_2.id,
            'bom_id': cls.bom_sub_1.id,
            'product_qty': 1.0,
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

    def test_01_non_material_costs_to_bom(self):
        """Test compute labor and overhead costs to BoM"""
        # Final Product Labor and Overhead Costs
        self.assertEqual(self.bom_top.standard_cost_labor, 50.0)
        self.assertEqual(self.bom_top.standard_cost_overhead, 35.0)
        # Sub-assembly Labor and Overhead Costs
        self.assertEqual(self.bom_sub_1.standard_cost_labor, 25.0)
        self.assertEqual(self.bom_sub_1.standard_cost_overhead, 70.0)

    def test_02_bom_standard_costs(self):
        """Test BoM standard costs computation."""
        # Final Product Total Cost =
        #   2 * (4* $10 + 1 * $15 + $95) + 3 * $20 + $85 = $445
        self.assertEqual(self.bom_top.standard_cost_total, 445.0)
        self.assertEqual(self.bom_top.standard_cost_material, 360.0)
        self.assertEqual(self.bom_top.standard_cost_only_material, 170.0)
        self.assertEqual(self.bom_top.standard_total_cost_labor, 100.0)
        self.assertEqual(self.bom_top.standard_total_cost_overhead, 175.0)
        # Sub-assembly Total Cost = 4* $10 + 1 * $15 + $95 = $150
        self.assertEqual(self.bom_sub_1.standard_cost_total, 150.0)
        self.assertEqual(self.bom_sub_1.standard_cost_material, 55.0)
        self.assertEqual(self.bom_sub_1.standard_cost_only_material, 55.0)
        self.assertEqual(self.bom_sub_1.standard_total_cost_labor, 25.0)
        self.assertEqual(self.bom_sub_1.standard_total_cost_overhead, 70.0)

    def test_03_manufacture_order(self):
        """Create Manufacture Order and check account move lines created"""
        mo = self.production_obj.create({
            'name': 'MO-01',
            'product_id': self.product_top.id,
            'product_uom_id': self.product_top.uom_id.id,
            'product_qty': 5.0,
            'bom_id': self.bom_top.id,
        })
        mo.action_assign()
        self._produce(mo, 2.0)
        account_move_lines = self.account_move_line_obj.search([
            ('manufacture_order_id', '=', mo.id)])
        self.assertEqual(len(account_move_lines), 4)
        for line in account_move_lines:
            if line['debit'] > 0.0:
                self.assertEqual(line.account_id, self.account_wip)
            elif line['credit'] > 0.0:
                if line.account_id == self.account_labor:
                    self.assertEqual(line.credit, 100.0)
                elif line.account_id == self.account_overhead:
                    self.assertEqual(line.credit, 70.0)

    def test_04_ubuild_order(self):
        """Create Unbuild Order and check account move lines created"""
        self.product_top.write({
            'standard_price': 445.0,
        })
        mo = self.production_obj.create({
            'name': 'MO-01',
            'product_id': self.product_top.id,
            'product_uom_id': self.product_top.uom_id.id,
            'product_qty': 5.0,
            'bom_id': self.bom_top.id,
        })
        mo.action_assign()
        self._produce(mo, 3.0)
        mo.button_mark_done()
        uo = self.unbuild_obj.create({
            'product_id': self.product_top.id,
            'bom_id': self.bom_top.id,
            'product_qty': 1.0,
            'product_uom_id': self.product_top.uom_id.id,
        })
        uo.action_unbuild()
        account_move_lines = self.account_move_line_obj.search([
            ('unbuild_order_id', '=', uo.id),
            ('product_id', 'in', [self.labor_1.id, self.overhead_1.id])
        ])
        self.assertEqual(len(account_move_lines), 4)
        for line in account_move_lines:
            if line['credit'] > 0.0:
                self.assertEqual(line.account_id, self.account_wip)
            elif line['debit'] > 0.0:
                if line.account_id == self.account_labor:
                    self.assertEqual(line.debit, 50.0)
                else:
                    self.assertEqual(line.debit, 35.0)
