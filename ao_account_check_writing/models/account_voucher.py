# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.tools import config
from openerp.addons.ao_account_check_writing.models.amount_to_text_en \
    import amount_to_text


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    @api.depends('amount')
    def _get_amount_in_word(self):
        for check in self:
            check.amount_in_word = amount_to_text(check.amount)

    check_number = fields.Char('Check Number')
    amount_in_word = fields.Char(compute='_get_amount_in_word', readonly=True,
                                 store=True)
    _sql_constraints = [
        ('check_per_journal_uniq', 'unique(check_number, journal_id)', 'Check Number Must be Unique Per Journal!'),
    ]

    @api.one
    def copy(self, default=None):
        if not default:
            default = {}
        default.update({'check_number': False})
        return super(AccountVoucher, self).copy(default=default)

    @api.multi
    def onchange_amount(self, amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id):
        """ Inherited - add amount_in_word and allow_check_writing in returned value dictionary """
        default = super(AccountVoucher, self).onchange_amount(amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id)
        if 'value' in default:
            amount = 'amount' in default['value'] and default['value']['amount'] or amount
            amount_in_word = amount_to_text(amount)
            default['value'].update({'amount_in_word':amount_in_word})
        return default

    @api.multi
    def print_check(self):
        if not self.ids:
            return {}

        check_layout_report = {
            'top': 'account.print.check.top',
            'middle': 'account.print.check.middle',
            'bottom': 'account.print.check.bottom',
        }

        check_layout = self[0].company_id.check_layout
        return {
            'type': 'ir.actions.report.xml',
            'report_name': check_layout_report[check_layout],
            'datas': {
                'model': 'account.voucher',
                'id': self.ids[0],
                'ids': self.ids,
                'report_type': 'pdf'
            },
            'nodestroy': True
        }
