# 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields


class TestAutoClosePo(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.po_obj = cls.env["purchase.order"]
        cls.product_obj = cls.env["product.product"]
        cls.partner_obj = cls.env["res.partner"]
        cls.invoice_obj = cls.env["account.invoice"]

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

    def _do_picking(self, picking, date):
        """Do picking with only one move on the given date."""
        picking.action_confirm()
        picking.force_assign()
        picking.move_lines.quantity_done = picking.move_lines.product_uom_qty
        picking.action_done()
        for move in picking.move_lines:
            move.date = date

    def test_01_auto_close_po(self):
        """Test if after processing a PO it gets automatically closed."""
        self.assertEqual(self.po.state, "draft")
        self.po.button_confirm()
        self._do_picking(self.po.picking_ids, fields.Datetime.now())
        self.assertEqual(self.po.qty_to_receive, 0.0)
        invoice = self.invoice_obj.create({
            "partner_id": self.partner.id,
            "purchase_id": self.po.id,
            "account_id": self.partner.property_account_payable_id.id,
            "type": "in_invoice",
        })
        invoice.purchase_order_change()
        invoice.action_invoice_open()
        self.assertEqual(self.po.qty_to_invoice, 0.0)
        # Invoice fully processed, now running cron:
        self.assertEqual(self.po.state, "purchase")
        self.po_obj.cron_ao_auto_close_purchases()
        self.assertEqual(self.po.state, "done")
