# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestCrmLeadReplyTo(SavepointCase):
    def setUp(cls):
        super(TestCrmLeadReplyTo, cls).setUp()
        cls.partner_obj = cls.env['res.partner']
        cls.lead_obj = cls.env['crm.lead']
        cls.team_obj = cls.env['crm.team']
        cls.env["ir.config_parameter"].sudo().set_param(
            "mail.catchall.domain", 'alephobjects.com')

        cls.partner = cls.partner_obj.create({
            'name': 'Mario Houses',
            'email': 'm.houses@customer.com',
        })
        cls.salesman = cls.env['res.partner'].create({
            'name': 'Test Salesman',
            'email': 'sales@example.com',
        })
        cls.lead = cls.lead_obj.create({
            'name': 'Interested in TAZ6',
            'partner_id': cls.partner.id,
        })
        cls.crm_team_1 = cls.team_obj.create({
            'name': 'Test CRM Team',
            'alias_name': 'test_crm_team',
            'reply_to_alias': True
        })
        crm_team_model = cls.env['ir.model'].search(
            [('model', '=', 'crm.team')])

        crm_lead_model = cls.env['ir.model'].search(
            [('model', '=', 'crm.lead')])

        cls.mail_alias = cls.env['mail.alias'].create({
            'alias_name': 'crm_team',
            'alias_model_id': crm_lead_model.id,
            'alias_parent_model_id': crm_team_model.id,
            'alias_parent_thread_id': cls.crm_team_1.id,
            'alias_defaults': "{'type': 'opportunity', 'team_id': %s}"
                              % cls.crm_team_1.id,
        })
        cls.crm_team_1.write({'alias_id': cls.mail_alias.id})

        cls.crm_salesman = cls.env['res.partner'].create({
            'name': 'Test CRM Salesman',
            'email': 'crm_salesman@example.com',
            'team_id': cls.crm_team_1.id
        })
        cls.team_lead = cls.lead_obj.create({
            'name': 'Interested in TAZ6 2',
            'partner_id': cls.partner.id,
            'team_id': cls.crm_team_1.id,
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
        message._notify(message, {}, force_send=True)
        self.assertEqual(
            message.email_from, 'LulzBot Sales<sales@lulzbot.com>')

    def test_02_send_email_with_crm_team_assigned(self):
        message = self.env['mail.message'].create({
            'subject': 'Message test 2',
            'author_id': self.crm_salesman.id,
            'email_from': self.crm_salesman.email,
            'message_type': 'email',
            'model': 'crm.lead',
            'res_id': self.team_lead.id,
            'partner_ids': [(4, self.partner.id)],
            'body': '<p>This is a test message</p>',
        })
        self.assertEqual(
            message.reply_to,
            'YourCompany Test CRM Team <crm_team@alephobjects.com>')
        message._notify(message, {}, force_send=True)
        self.assertEqual(
            message.email_from,
            'YourCompany Test CRM Team <crm_team@alephobjects.com>')
