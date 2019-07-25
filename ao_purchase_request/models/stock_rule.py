# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _make_pr_get_domain(self, values):
        super(StockRule, self)._make_pr_get_domain(values)
        domain = (('id', '=', 0),)
        return domain
