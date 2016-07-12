# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _
import datetime


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    days_overdue = fields.Integer(compute='_compute_days_overdue',
                                  search='_search_days_overdue',
                                  string='Days overdue')

    @api.depends('date_maturity')
    def _compute_days_overdue(self):
        today_date = fields.Date.from_string(fields.Date.today())
        for line in self:
            if line.date_maturity and line.amount_residual:
                date_maturity = fields.Date.from_string(
                    line.date_maturity)
                days_overdue = (today_date - date_maturity).days
                if days_overdue > 0:
                    line.days_overdue = days_overdue

    def _search_days_overdue(self, operator, value):
        due_date = fields.Date.from_string(fields.Date.today()) - \
                   datetime.timedelta(days=value)
        if operator in ('!=', '<>', 'in', 'not in'):
            raise ValueError('Invalid operator: %s' % (operator,))
        if operator == '>':
            operator = '<'
        elif operator == '<':
            operator = '>'
        elif operator == '>=':
            operator = '<='
        elif operator == '<=':
            operator = '>='
        return [('date_maturity', operator, due_date)]
