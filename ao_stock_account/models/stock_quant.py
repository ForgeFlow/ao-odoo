# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.cr_uid_ids_context
    def external_price_update(self, cr, uid, quant_ids, newprice):
        self._price_update(cr, uid, quant_ids, newprice, context=None)
        return True
