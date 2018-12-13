# 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestAoBase(common.TransactionCase):

    def setUp(self):
        super(TestAoBase, self).setUp()
        self.partner_obj = self.env['res.partner']

        self.user = self.env.ref('base.user_demo')
        self.colorado = self.env.ref('base.state_us_6')
        self.us_country = self.env.ref('base.us')

    def test_01_deactivation_propagates(self):
        """Deactivating user to see if corresponding partner does too."""
        self.assertTrue(self.user.active)
        self.assertTrue(self.user.partner_id.active)
        self.user.active = False
        self.assertFalse(self.user.active)
        self.assertFalse(self.user.partner_id.active)

    def test_02_onchange_state(self):
        """State input should auto-fill country in contract info."""
        partner = self.partner_obj.new({
            'name': 'Test',
            'state_id': self.colorado.id,
        })
        partner.onchange_state()
        self.assertEqual(partner.country_id, self.us_country)
