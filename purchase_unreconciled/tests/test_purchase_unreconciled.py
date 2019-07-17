# 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields


class TestPurchaseUnreconciled(common.SingleTransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.po_obj = cls.env["purchase.order"]
        cls.product_obj = cls.env["product.product"]
        cls.category_obj = cls.env["product.category"]
        cls.partner_obj = cls.env["res.partner"]
        cls.acc_obj = cls.env["account.account"]
        cls.invoice_obj = cls.env["account.invoice"]

        assets = cls.env.ref("account.data_account_type_current_assets")

        # Create partner:
        cls.partner = cls.partner_obj.create({
            "name": "Test Vendor",
        })
        # Create standard product:
        cls.product = cls.product_obj.create({
            "name": "Purchased Product",
            "type": "product",
        })
        # Create product that uses a reconcilable stock input account.
        cls.account = cls.acc_obj.create({
            "name": "Test stock input account",
            "code": 9999,
            "user_type_id": assets.id,
            "reconcile": True,
        })
        product_categ = cls.category_obj.create({
            "name": "Test Category",
            "property_stock_account_input_categ_id": cls.account.id,
        })
        cls.product_to_reconcile = cls.product_obj.create({
            "name": "Purchased Product (To reconcile)",
            "type": "product",
            "categ_id": product_categ.id,
        })

        # Create PO's:
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
        cls.po_2 = cls.po_obj.create({
            "partner_id": cls.partner.id,
            "order_line": [(0, 0, {
                "product_id": cls.product_to_reconcile.id,
                "name": cls.product_to_reconcile.name,
                "product_qty": 5.0,
                "price_unit": 100.0,
                "product_uom": cls.product_to_reconcile.uom_id.id,
                "date_planned": fields.Datetime.now(),
            })],
        })

    def _do_picking(self, picking, date):
        """Do picking with only one move on the given date."""
        picking.action_confirm()
        picking.force_assign()
        picking.move_lines.quantity_done = picking.move_lines.product_uom_qty
        picking.action_done()
        for move in picking.move_lines:
            move.date = date

    def test_01_nothing_to_reconcile(self):
        """Test that unreconciled using un-reconcilable account."""
        po = self.po
        self.assertEqual(po.state, "draft")
        po.button_confirm()
        self._do_picking(po.picking_ids, fields.Datetime.now())
        self.assertFalse(po.unreconciled)
        # Invoice created and validated:
        invoice = self.invoice_obj.create({
            "partner_id": self.partner.id,
            "purchase_id": po.id,
            "account_id": self.partner.property_account_payable_id.id,
            "type": "in_invoice",
        })
        invoice.purchase_order_change()
        invoice.action_invoice_open()
        self.assertEqual(po.state, "purchase")
        self.assertFalse(po.unreconciled)

    def test_02_to_reconcile(self):
        """Test that unreconciled using reconcilable account."""
        po = self.po_2
        self.assertEqual(po.state, "draft")
        po.button_confirm()
        self._do_picking(po.picking_ids, fields.Datetime.now())
        self.assertFalse(po.unreconciled)
        # Invoice created and validated:
        invoice = self.invoice_obj.create({
            "partner_id": self.partner.id,
            "purchase_id": po.id,
            "account_id": self.partner.property_account_payable_id.id,
            "type": "in_invoice",
        })
        invoice.purchase_order_change()
        invoice.action_invoice_open()
        self.assertEqual(po.state, "purchase")
        self.assertTrue(po.unreconciled)

    def test_03_search_unreconciled(self):
        """Test searching unreconciled PO's."""
        res = self.po_obj.search([("unreconciled", "=", True)])
        self.assertNotIn(self.po, res)
        self.assertIn(self.po_2, res)
        # Test value error:
        with self.assertRaises(ValueError):
            self.po_obj.search([("unreconciled", "=", "true")])
