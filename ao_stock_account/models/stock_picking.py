# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        res = super(StockPicking, self)._get_invoice_vals(key, inv_type,
                                                          journal_id, move)
        if move.picking_id.origin:
            res['origin'] = \
                move.picking_id.name + (move.picking_id.origin and
                                        (':' + move.picking_id.origin) or '')
        return res
