# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common
from odoo.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class TestAoProduct(common.TransactionCase):

    def setUp(self):
        super(TestAoProduct, self).setUp()
        self.user_obj = self.env['res.users']
        self.product_obj = self.env['product.product']
        self.template_obj = self.env['product.template']

        self.product = self.env.ref('product.product_product_11')
        self.template = self.product.product_tmpl_id

        self.maintainer = self.user_obj.create({
            'login': 'test-maintainer',
            'name': 'Test Maintainer',
            'email': 'test-maintainer@example.org',
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.env.ref('stock.group_stock_user').id),
                (4, self.env.ref('ao_product.group_product_maintainer').id),
            ]
        })
        self.user = self.user_obj.create({
            'login': 'test-user',
            'name': 'Test User',
            'email': 'test-maintainer@example.org',
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.env.ref('stock.group_stock_manager').id),
            ]
        })

    def test_01_actions(self):
        """Call view actions to ensure there is no error."""
        self.product.action_view_stock_moves()
        self.template.action_view_stock_moves()

    def test_02_security_create(self):
        """Test who can create products."""
        self.product_obj.sudo(self.maintainer).create({
            'name': 'TEST Product',
            'type': 'service',
        })
        with self.assertRaises(ValidationError):
            self.product_obj.sudo(self.user).create({
                'name': 'TEST Product',
                'type': 'service',
            })
        # Admin user should overpass all rules:
        self.product_obj.sudo().create({
            'name': 'TEST Product',
            'type': 'service',
        })

    def test_03_security_write(self):
        """Test write security on products."""
        self.product.sudo(self.maintainer).write({
            'standard_price': 30.0,
        })
        with self.assertRaises(ValidationError):
            self.product.sudo(self.user).write({
                'standard_price': 30.0,
            })
        # Admin user should overpass all rules:
        self.product_obj.sudo().write({
            'standard_price': 30.0,
        })
