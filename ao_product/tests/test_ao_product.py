# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestAoProduct(common.TransactionCase):

    def setUp(self):
        super(TestAoProduct, self).setUp()
        self.product = self.env.ref('product.product_product_11')
        self.template = self.product.product_tmpl_id

    def test_01_actions(self):
        """Call view actions to ensure there is no error."""
        self.product.action_view_stock_moves()
        self.template.action_view_stock_moves()
