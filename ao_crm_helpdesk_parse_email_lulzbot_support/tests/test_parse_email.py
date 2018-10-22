# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.modules.module import get_module_resource


class TestParseEmailLulzbot(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestParseEmailLulzbot, self).setUp(*args, **kwargs)
        self.partner_obj = self.env['res.partner']
        self.helpdesk_obj = self.env['crm.helpdesk']

        request_file = open(get_module_resource(
            'ao_crm_helpdesk_parse_email_lulzbot_support',
            'tests', 'test_message.eml'), 'rb')
        self.test_message = request_file.read()

    def test_01_pase_email(self):
        self.helpdesk_obj.message_process('crm.helpdesk', self.test_message)
        ticket = self.helpdesk_obj.search(
            [('email_from', '=', 'james.k@customer.com'),
             ('contact_name', '=', 'James Knight')],
            limit=1)
        self.assertTrue(ticket)
        self.assertFalse(ticket.partner_id)

    def test_02_pase_email_existing_partner(self):
        partner = self.partner_obj.create({
            'name': 'James Knight',
            'email': 'james.k@customer.com',
        })
        self.helpdesk_obj.message_process('crm.helpdesk', self.test_message)
        ticket = self.helpdesk_obj.search(
            [('email_from', '=', 'james.k@customer.com'),
             ('contact_name', '=', 'James Knight')])
        self.assertTrue(ticket)
        self.assertEqual(ticket.partner_id, partner)
