# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import ast

from odoo import fields, models
from datetime import datetime


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    date_wizard = fields.Date(
        'Inventory at Selected Date',
        help="Choose a date to get the inventory at that date",
        default=fields.Date.context_today
    )

    def open_table(self):
        self.ensure_one()
        if self.compute_at_date:
            self.date = datetime.strptime(
                "%s %s" % (self.date_wizard, "23:59:00"),
                '%Y-%m-%d %H:%M:%S')
        res = super(StockQuantityHistory, self).open_table()
        ctx = res['context']
        if isinstance(ctx, str):
            ctx = ast.literal_eval(ctx)
        res.update({
            'context': dict(ctx, to_date=self.date)
        })
        return res
