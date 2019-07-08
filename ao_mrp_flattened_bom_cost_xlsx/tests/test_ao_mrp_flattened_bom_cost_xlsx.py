# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# - Lois Rilo <lois.rilo@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestReportXlsxAoBomCost(TransactionCase):

    def setUp(self):
        super(TestReportXlsxAoBomCost, self).setUp()
        report_object = self.env["ir.actions.report"]
        self.bom = self.env.ref("mrp.mrp_bom_manufacture")

        report_name = "mrp_flattened_bom_cost_xlsx.flattened_bom_xlsx"
        self.report = report_object._get_report_from_name(report_name)

    def test_01_render_report(self):
        report = self.report
        self.assertEqual(report.report_type, "xlsx")
        report.render(self.bom.ids, {})
