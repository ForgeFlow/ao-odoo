# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestHelpdeskPriority(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestHelpdeskPriority, self).setUp(*args, **kwargs)
        self.partner_obj = self.env["res.partner"]
        self.helpdesk_obj = self.env["crm.helpdesk"]

        self.test_partner = self.partner_obj.create({
            "name": "Jamal Murray",
            "email": "jamal.murray@test.com"
        })
        self.contact_name = "Torrey Craig"
        self.test_email = "torrey.craig@test.com"

    def test_01_suggest_recipient_partner(self):
        partner = self.test_partner
        ticket = self.helpdesk_obj.create({
            "name": "Problem with TAZ6",
            "partner_id": partner.id,
        })
        res = ticket.message_get_suggested_recipients()
        suggestion = res.get(ticket.id, False)
        self.assertTrue(suggestion)
        self.assertEqual(suggestion[0][0], partner.id)
        self.assertEqual(
            suggestion[0][1],
            "%s<%s>" % (partner.name, partner.email),
        )
        self.assertEqual(suggestion[0][2], "Partner")

    def test_02_suggest_recipient_email(self):
        ticket = self.helpdesk_obj.create({
            "name": "Problem with TAZ6",
            "contact_name": self.contact_name,
            "email_from": self.test_email,
        })
        res = ticket.message_get_suggested_recipients()
        suggestion = res.get(ticket.id, False)
        self.assertTrue(suggestion)
        self.assertEqual(suggestion[0][0], False)
        self.assertEqual(suggestion[0][1], self.test_email)
        self.assertEqual(suggestion[0][2], "Partner Email")
