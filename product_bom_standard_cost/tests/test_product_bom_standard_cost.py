# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestProductBomStandardCost(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductBomStandardCost, cls).setUpClass()

        cls.product_obj = cls.env['product.product']
        cls.bom_obj = cls.env['mrp.bom']
        cls.bom_line_obj = cls.env['mrp.bom.line']

        # Create products:
        cls.product_top = cls.product_obj.create({
            'name': 'Final Product',
            'type': 'product',
        })
        cls.product_sub_1 = cls.product_obj.create({
            'name': 'L01-01',
            'type': 'product',
            'standard_price': 100.0,
        })
        cls.component_1 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 10.0,
        })
        cls.component_2 = cls.product_obj.create({
            'name': 'RM 01',
            'type': 'product',
            'standard_price': 15.0,
        })
        cls.component_3 = cls.product_obj.create({
            'name': 'RM 03',
            'type': 'product',
            'standard_price': 20.0,
        })

        # Create Bills of Materials:
        cls.bom_top = cls.bom_obj.create({
            'product_tmpl_id': cls.product_top.product_tmpl_id.id,

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

    def test_01_bom_standard_cost(self):
        """Test BoM standard cost computation."""
        # Final Product = 2 * (4* $10 + 1 * $15) + 3 * $20 = $170
        self.assertEqual(self.product_top.bom_standard_cost, 170.0)
        # Sub-assembly = 4* $10 + 1 * $15 = $55
        self.assertEqual(self.product_sub_1.bom_standard_cost, 55.0)
