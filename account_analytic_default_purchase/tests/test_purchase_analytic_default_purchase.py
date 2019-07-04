# 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo import fields


class TestPurchaseAnalyticDefault(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPurchaseAnalyticDefault, cls).setUpClass()

        cls.product_obj = cls.env["product.product"]
        cls.po_obj = cls.env["purchase.order"]
        cls.partner_obj = cls.env["res.partner"]
        cls.aa_obj = cls.env["account.analytic.account"]

        # Create partner, analytic account, default and product.
        cls.partner = cls.partner_obj.create({
            "name": "Test Vendor",
        })
        cls.analytic_acc = cls.aa_obj.create({
            "name": "Some Vendors account",
        })
        cls.env["account.analytic.default"].create({
            "analytic_id": cls.analytic_acc.id,
            "partner_id": cls.partner.id,
        })
        cls.product_1 = cls.product_obj.create({
            "name": "Purchased product AA01",
            "type": "product",
        })

    def test_01_standard_cost(self):
        po = self.po_obj.create({
            "partner_id": self.partner.id,
            "order_line": [
                (0, 0, {
                    "name": "po line",
                    "price_unit": 1000.0,
                    "purchase_price": 700.0,
                    "product_qty": 10.0,
                    "product_uom": self.product_1.uom_id.id,
                    "date_planned": fields.Datetime.now(),
                    "product_id": self.product_1.id})],
        })
        self.assertFalse(po.order_line.account_analytic_id)
        po.order_line._onchange_product_id_analytic_default()
        self.assertTrue(po.order_line.account_analytic_id)
