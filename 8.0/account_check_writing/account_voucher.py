# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from lxml import etree
from openerp import models, fields, api, _
from openerp.addons.account_check_writing.amount_to_text_en import amount_to_text

class account_voucher(models.Model):
    _inherit = 'account.voucher'
    
    @api.model
    def _get_currency(self):
        res = super(account_voucher, self)._get_currency()
        if not res:
            res = self.env.user.company_id.currency_id.id
        return res
    
    @api.model
    def _make_journal_search(self, ttype):
        journal_pool = self.env['account.journal']
        if self.env.context.get('write_check', False) :
            return journal_pool.search([('allow_check_writing', '=', True)], limit=1)
        return journal_pool.search([('type', '=', ttype)], limit=1)
    
    @api.depends('amount')
    def _get_amount_in_word(self):
        for check in self:
            check.amount_in_word = amount_to_text(check.amount)
    
    amount_in_word = fields.Char(compute='_get_amount_in_word', readonly=True, store=True)
    allow_check = fields.Boolean(related='journal_id.allow_check_writing', string='Allow Check Writing')
    check_number = fields.Char('Check Number')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True, states={'draft':[('readonly', False)]})
    check_done = fields.Boolean(string='Check Printed')

    _sql_constraints = [
        ('check_per_journal_uniq', 'unique(check_number, journal_id)', 'Check Number Must be Unique Per Journal!'),
    ]
    
    @api.multi
    def onchange_amount(self, amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id):
        """ Inherited - add amount_in_word and allow_check_writing in returned value dictionary """
        default = super(account_voucher, self).onchange_amount(amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id)
        if 'value' in default:
            amount = 'amount' in default['value'] and default['value']['amount'] or amount
            amount_in_word = amount_to_text(amount)
            default['value'].update({'amount_in_word':amount_in_word})
            if journal_id:
                allow_check_writing = self.env['account.journal'].browse(journal_id).allow_check_writing
                default['value'].update({'allow_check': allow_check_writing})
        return default
    
    @api.multi
    def onchange_journal(self, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id):
        vals = super(account_voucher, self).onchange_journal(journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id)
        if vals and not vals.get('value', {})['currency_id']:
            vals['value']['currency_id'] = self.env.user.company_id.currency_id.id
        return vals
    
    @api.one
    def copy(self, default=None):
        if not default:
            default = {}
        default.update({'check_number': False})
        return super(account_voucher, self).copy(default=default)
    
    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        """
            Add domain 'allow_check_writing = True' on journal_id field and remove 'widget = selection' on the same
            field because the dynamic domain is not allowed on such widget
        """
        res = super(account_voucher, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        nodes = doc.xpath("//field[@name='journal_id']")
        if self.env.context.get('write_check', False) :
            for node in nodes:
                node.set('domain', "[('type', '=', 'bank'), ('allow_check_writing','=',True)]")
                node.set('widget', '')
            res['arch'] = etree.tostring(doc)
        return res
    
    @api.multi
    def print_check(self):
        self.ensure_one()
        value = {}
        check_layout_report = {
            'top' : 'account.print.check.top',
            'middle' : 'account.print.check.middle',
            'bottom' : 'account.print.check.bottom',
        }
        if self.check_number or self.journal_id.use_preprint_check :
            check_layout = self.company_id.check_layout
            value = {
                 'type': 'ir.actions.report.xml',
                 'report_name':check_layout_report[check_layout],
                 'datas': {
                     'model':'account.voucher',
                     'id': self.id or False,
                     'ids': self.ids or [],
                     'report_type': 'pdf'
                 },
                 'nodestroy': True
             }
        else:
            form_view = self.env.ref('account_check_writing.view_account_check_write')
            value = {
                'name': _('Print Check'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.check.write',
                'views': [(form_view and form_view.id or False, 'form'), (False, 'tree')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': self.env.context,
            }
        return value

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: