# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    # TODO: to remove?
    @api.cr_uid_context
    def get_first_move(self, cr, uid, quant_id, context=None):
        quant = self.pool['stock.quant'].browse(cr, uid, quant_id,
                                                context=context)
        move = False
        for m in quant.history_ids:
            if not move or m.date < move.date:
                move = m
        return move.id
