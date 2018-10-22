# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestCrmLeadReplyTo(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestCrmLeadReplyTo, self).setUp(*args, **kwargs)
        self.partner_obj = self.env['res.partner']
        self.lead_obj = self.env['crm.lead']

        self.partner = self.partner_obj.create({
            'name': 'Mario Houses',
            'email': 'm.houses@customer.com',
        })
        self.salesman = self.env['res.partner'].create({
            'name': 'Test Salesman',
            'email': 'sales@example.com',
        })
        self.lead = self.lead_obj.create({
            'name': 'Interested in TAZ6',
            'partner_id': self.partner.id,
        })

    def test_01_send_email(self):
        message = self.env['mail.message'].create({
            'subject': 'Message test',
            'author_id': self.salesman.id,
            'email_from': self.salesman.email,
            'message_type': 'email',
            'model': 'crm.lead',
            'res_id': self.lead.id,
            'partner_ids': [(4, self.partner.id)],
            'body': '<p>This is a test message</p>',
        })
        self.assertEqual(message.reply_to, 'sales@lulzbot.com')
        self.assertEqual(
            message.email_from, 'LulzBot Sales<sales@lulzbot.com>')
