# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def update_amount_residual(self):
        """Hook method used in the script t_12963."""
        super(AccountMoveLine, self)._amount_residual()
        return True
