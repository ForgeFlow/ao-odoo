# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestAoStock(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.report_wiz = cls.env["stock.quantity.history"]

    def test_01_inventory_valuation_report_customization(self):
        """Test date is set to end of the given day."""
        wiz = self.report_wiz.create({
            "compute_at_date": 1,
        })
        self.assertTrue(wiz.date_wizard)
        wiz.open_table()
        self.assertTrue(wiz.date.hour, 23)
        self.assertTrue(wiz.date.minute, 59)
