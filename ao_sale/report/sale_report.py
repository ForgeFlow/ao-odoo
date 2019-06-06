# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    tag_id = fields.Many2one('crm.lead.tag', 'Tags', readonly=True)

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , strel.tag_id as tag_id
            """
        return select_str

    def _from(self):
        select_str = super(SaleReport, self)._from()
        select_str += """
            LEFT JOIN sale_order_tag_rel strel ON s.id = strel.order_id
            """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", strel.tag_id"
        return group_by_str
