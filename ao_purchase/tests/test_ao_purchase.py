# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# - Lois Rilo <lois.rilo@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields
from odoo.exceptions import UserError


class TestAoPurchase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.po_obj = cls.env["purchase.order"]
        cls.product_obj = cls.env["product.product"]
        cls.partner_obj = cls.env["res.partner"]
        cls.invoice_obj = cls.env["account.invoice"]
        cls.user_obj = cls.env['res.users'].with_context(
            no_reset_password=True)
        report_object = cls.env["ir.actions.report"]

        # Get PO reports.
        cls.rfq_report = report_object._get_report_from_name(
            "purchase.report_purchasequotation")
        cls.po_report = report_object._get_report_from_name(
            "purchase.report_purchaseorder")

        # Set company params:
        company = cls.env.ref("base.main_company")
        company.po_double_validation = "two_step"
        company.po_double_validation_amount = 100.0

        # Purchase users:
        user = cls.env.ref("purchase.group_purchase_user")
        manager = cls.env.ref("purchase.group_purchase_manager")
        cls.po_user = cls.user_obj.create({
            "name": "Nikola Jokic",
            "login": "nikola",
            "email": "nikola@test.com",
            "groups_id": [(6, 0, [user.id])]
        })
        cls.po_manager = cls.user_obj.create({
            "name": "Paul Millsap",
            "login": "paul",
            "email": "paul@test.com",
            "groups_id": [(6, 0, [manager.id])]
        })

        # Create partner and product:
        cls.partner = cls.partner_obj.create({
            "name": "Test Vendor",
        })
        cls.product = cls.product_obj.create({
            "name": "Purchased Product",
            "type": "product",
        })

        # Create PO:
        cls.po = cls.po_obj.create({
            "partner_id": cls.partner.id,
            "order_line": [(0, 0, {
                "product_id": cls.product.id,
                "name": cls.product.name,
                "product_qty": 5.0,
                "price_unit": 100.0,
                "product_uom": cls.product.uom_id.id,
                "date_planned": fields.Datetime.now(),
            })],
        })

    def test_01_restrict_po_print_statuses(self):
        """Test only be able to print in certain states."""
        self.assertEqual(self.po.state, "draft")
        self.rfq_report.render(self.po.ids, {})
        with self.assertRaises(UserError):
            self.po_report.render(self.po.ids, {})

        self.po.sudo(self.po_user).button_confirm()
        self.assertEqual(self.po.state, "to approve")
        with self.assertRaises(UserError):
            self.rfq_report.render(self.po.ids, {})

        self.po.sudo(self.po_manager).button_approve()
        self.assertEqual(self.po.state, "purchase")
        self.po_report.render(self.po.ids, {})
        self.rfq_report.render(self.po.ids, {})
