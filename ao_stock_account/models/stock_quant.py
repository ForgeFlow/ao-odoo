# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, SUPERUSER_ID


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.cr_uid_ids_context
    def external_price_update(self, cr, uid, quant_ids, newprice, date):
        context = {}
        for quant in self.browse(cr, uid, quant_ids, context=context):
            move = self._get_latest_move(cr, uid, quant, context=context)
            valuation_update = newprice - quant.cost
            # this is where we post accounting entries for adjustment,
            # if needed
            if not quant.company_id.currency_id.is_zero(valuation_update):
                ctx = dict(context, force_valuation_amount=valuation_update)
                ctx = dict(ctx, force_period_date=date)
                self._account_entry_move(cr, uid, [quant], move,
                                         context=ctx)
            self.write(cr, SUPERUSER_ID, [quant.id], {'cost': newprice},
                       context=context)
        return True
