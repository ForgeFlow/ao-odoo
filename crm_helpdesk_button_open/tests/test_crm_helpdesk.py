# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestCrmHelpdeskButtonOpen(common.TransactionCase):

    def setUp(self):
        super(TestCrmHelpdeskButtonOpen, self).setUp()
        self.obj_helpdesk = self.env['crm.helpdesk']
        self.obj_user = self.env['res.users'].with_context(
            no_reset_password=True)
        # groups
        self.group_sale_salesman = self.env.ref(
            'sales_team.group_sale_salesman')
        # company
        self.company1 = self.env.ref('base.main_company')
        # Create users
        self.user1_id = self._create_user('user_1',
                                          [self.group_sale_salesman],
                                          self.company1)

    def _create_user(self, login, groups, company):
        """ Create a user."""
        group_ids = [group.id for group in groups]
        user = \
            self.obj_user.with_context({'no_reset_password': True}).create({
                'name': 'Test User',
                'login': login,
                'password': 'demo',
                'email': 'test@yourcompany.com',
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': [(6, 0, group_ids)]
            })
        return user.id

    def test_crm_helpdesk_set_open(self):
        vals = {
            'name': 'Test',
            'user_id': False,
        }
        crm_helpdesk = self.obj_helpdesk.create(vals)
        crm_helpdesk.sudo(self.user1_id).button_open()
        self.assertEqual(
            crm_helpdesk.state, 'open',
            'Helpdesk ticket should be in state open')
        self.assertEqual(crm_helpdesk.user_id.id, self.user1_id,
                         'Helpdesk ticket should be assigned to Test User')
