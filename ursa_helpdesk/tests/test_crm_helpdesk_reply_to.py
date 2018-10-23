# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestCrmHelpdeskReplyTo(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestCrmHelpdeskReplyTo, self).setUp(*args, **kwargs)
        self.partner_obj = self.env['res.partner']
        self.helpdesk_obj = self.env['crm.helpdesk']

        self.partner = self.partner_obj.create({
            'name': 'Emma Smith',
            'email': 'e.smith@customer.com',
        })
        self.salesman = self.env['res.partner'].create({
            'name': 'Test Salesman',
            'email': 'sales@example.com',
        })
        self.ticket = self.helpdesk_obj.create({
            'name': 'Problem with TAZ6',
            'partner_id': self.partner.id,
        })

    def test_01_send_email(self):
        message = self.env['mail.message'].create({
            'subject': 'Message test',
            'author_id': self.salesman.id,
            'email_from': self.salesman.email,
            'message_type': 'email',
            'model': 'crm.helpdesk',
            'res_id': self.ticket.id,
            'partner_ids': [(4, self.partner.id)],
            'body': '<p>This is a test message</p>',
        })
        self.assertEqual(message.reply_to, 'support@lulzbot.com')
        self.assertEqual(
            message.email_from, 'LulzBot Support <support@lulzbot.com>')
