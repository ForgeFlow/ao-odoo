# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    maturity_residual = fields.Float(
        compute='_maturity_residual', string="Residual Amount",
        help="The residual amount on a receivable or payable of a journal "
             "entry expressed in the company currency.")

    @api.multi
    @api.depends('date_maturity', 'debit', 'credit')
    def _maturity_residual(self):
        """
            inspired by amount_residual
        """
        for move_line in self:
            sign = (move_line.debit - move_line.credit) < 0 and -1 or 1
            move_line.maturity_residual = move_line.amount_residual * sign
