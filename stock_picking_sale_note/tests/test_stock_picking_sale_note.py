# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields


class TestStockPickingSaleNote(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.so_obj = cls.env["sale.order"]
        cls.product_obj = cls.env["product.product"]
        cls.partner_obj = cls.env["res.partner"]

        # Create partner and product:
        cls.partner = cls.partner_obj.create({
            "name": "Test Vendor",
        })
        cls.product = cls.product_obj.create({
            "name": "Best seller Product",
            "type": "product",
        })

        # Create SO:
        cls.so = cls.so_obj.create({
            "partner_id": cls.partner.id,
            "order_line": [(0, 0, {
                "product_id": cls.product.id,
                "name": cls.product.name,
                "product_qty": 5.0,
                "price_unit": 200.0,
                "product_uom": cls.product.uom_id.id,
                "date_planned": fields.Datetime.now(),
            })],
            "note": "Test note."
        })

    def _do_picking(self, picking, date):
        """Do picking with only one move on the given date."""
        picking.action_confirm()
        picking.action_assign()
        picking.move_lines.quantity_done = picking.move_lines.product_uom_qty
        picking.action_done()
        for move in picking.move_lines:
            move.date = date

    def test_01_sale_note(self):
        """Sale note passed to picking."""
        self.assertEqual(self.so.state, "draft")
        self.so.action_confirm()
        # self._do_picking(self.po.picking_ids, fields.Datetime.now())
        self.assertEqual(self.so.state, "sale")
        picking = self.so.picking_ids
        self.assertEqual(picking.sale_order_origin, True)
        self.assertEqual(picking.sale_note, self.so.note)
