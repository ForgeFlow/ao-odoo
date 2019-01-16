# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestHelpdeskPriority(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestHelpdeskPriority, self).setUp(*args, **kwargs)
        self.partner_obj = self.env['res.partner']
        self.helpdesk_obj = self.env['crm.helpdesk']

        self.partner_company = self.partner_obj.create({
            'name': 'Company',
            'is_company': True,
            'helpdesk_default_priority': '2',
        })
        self.partner_contact_1 = self.partner_obj.create({
            'name': 'Contact 1',
            'is_company': False,
            'parent_id': self.partner_company.id,
        })
        self.partner_contact_2 = self.partner_obj.create({
            'name': 'Contact 2',
            'is_company': False,
            'helpdesk_default_priority': '0',
        })

    def test_default_ticket_priority(self):
        self.ticket_1 = self.helpdesk_obj.create({
            'name': 'Problem with TAZ6',
            'partner_id': self.partner_contact_1.id,
        })
        self.ticket_2 = self.helpdesk_obj.create({
            'name': 'Problem with TAZ6',
            'partner_id': self.partner_contact_2.id,
        })
        self.ticket_1._onchange_partner_id()
        self.ticket_2._onchange_partner_id()
        self.assertEqual(self.ticket_1.priority, '2')
        self.assertEqual(self.ticket_2.priority, '0')
