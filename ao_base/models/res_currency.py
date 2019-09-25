# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Currency(models.Model):
    _inherit = "res.currency"

    @api.multi
    def amount_to_text(self, amount):
        res = super().amount_to_text(amount)
        res = res.replace(' And', '')
        return res
