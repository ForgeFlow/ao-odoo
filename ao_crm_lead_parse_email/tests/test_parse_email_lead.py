# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.modules.module import get_module_resource


class TestParseEmailLead(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestParseEmailLead, self).setUp(*args, **kwargs)
        self.partner_obj = self.env['res.partner']
        self.lead_obj = self.env['crm.lead']
        self.campaign = self.env['utm.campaign'].create(
            {'name': 'test_cpg_1'})
        self.medium = self.env.ref('utm.utm_medium_email')
        self.source = self.env['utm.source'].create(
            {'name': 'test_src_1'})
        request_file = open(get_module_resource(
            'ao_crm_lead_parse_email',
            'tests', 'test_message.eml'), 'rb')
        self.test_message = request_file.read()

    def test_01_pase_email(self):
        self.lead_obj.message_process('crm.lead', self.test_message)
        lead = self.lead_obj.search(
            [('email_from', '=', 'laura.f@customer.com'),
             ('contact_name', '=', 'Laura Fincher')],
            limit=1)
        self.assertTrue(lead)
        self.assertFalse(lead.partner_id)

    def test_02_pase_email_existing_partner(self):
        partner = self.partner_obj.create({
            'name': 'Laura Fincher',
            'email': 'laura.f@customer.com',
        })
        self.lead_obj.message_process('crm.lead', self.test_message)
        lead = self.lead_obj.search(
            [('email_from', '=', 'laura.f@customer.com'),
             ('contact_name', '=', 'Laura Fincher')])
        self.assertTrue(lead)
        self.assertEqual(lead.partner_id, partner)
        self.assertEqual(lead.campaign_id, self.campaign)
        self.assertEqual(lead.medium_id, self.medium)
        self.assertEqual(lead.source_id, self.source)
