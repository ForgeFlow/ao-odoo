# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# - Lois Rilo <lois.rilo@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestReportXlsxAoBomStructure(TransactionCase):

    def setUp(self):
        super(TestReportXlsxAoBomStructure, self).setUp()
        report_object = self.env['ir.actions.report']
        self.bom = self.env.ref("mrp.mrp_bom_manufacture")

        report_name = 'ao_mrp_bom_structure_xlsx.bom_structure_xlsx'
        self.report = report_object._get_report_from_name(report_name)

    def test_01_render_report(self):
        report = self.report
        self.assertEqual(report.report_type, 'xlsx')
        report.render(self.bom.ids, {})
