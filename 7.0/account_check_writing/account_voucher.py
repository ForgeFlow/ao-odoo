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
from openerp.osv import osv,fields
from openerp.tools.translate import _
from openerp.addons.account_check_writing.amount_to_text_en import amount_to_text


class account_voucher(osv.Model):
    _inherit = 'account.voucher'

    def _get_currency(self, cr, uid, context=None):
        res = super(account_voucher, self)._get_currency(cr, uid, context)
        if not res:
            user_pool = self.pool.get("res.users")
            res = user_pool.browse(cr, uid, uid).company_id.currency_id.id
        return res

    def _make_journal_search(self, cr, uid, ttype, context=None):
        if context is None: 
            context = {}
        journal_pool = self.pool.get('account.journal')
        if context.get('write_check',False) :
            return journal_pool.search(cr, uid, [('allow_check_writing', '=', True)], limit=1)
        return journal_pool.search(cr, uid, [('type', '=', ttype)], limit=1)

    def _get_amount_in_word(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for check in self.browse(cr, uid, ids, context=context):
            res.update({check.id: amount_to_text(check.amount)})
        return res
    
    _columns = {
        'amount_in_word': fields.function(_get_amount_in_word, type='char', readonly=True, store=True),
        'allow_check' : fields.related('journal_id', 'allow_check_writing', type='boolean', string='Allow Check Writing'),
        'check_number': fields.char('Check Number', size=32),
        'journal_id':fields.many2one('account.journal', 'Journal', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'check_done': fields.boolean("Check Printed")
    }

    _sql_constraints = [
        ('check_per_journal_uniq', 'unique(check_number, journal_id)', 'Check Number Must be Unique Per Journal!'),
    ]

    def onchange_amount(self, cr, uid, ids, amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id, context=None):
        """ Inherited - add amount_in_word and allow_check_writing in returned value dictionary """
        if not context:
            context = {}
        default = super(account_voucher, self).onchange_amount(cr, uid, ids, amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id, context=context)
        if 'value' in default:
            amount = 'amount' in default['value'] and default['value']['amount'] or amount
            amount_in_word = amount_to_text(amount)
            default['value'].update({'amount_in_word':amount_in_word})
            if journal_id:
                allow_check_writing = self.pool.get('account.journal').browse(cr, uid, journal_id, context=context).allow_check_writing
                default['value'].update({'allow_check':allow_check_writing})
        return default

    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=None):
        vals = super(account_voucher, self).onchange_journal(cr, uid, ids, journal_id, line_ids, tax_id,partner_id, date, amount, ttype, company_id, context=context)
        if vals and not vals.get('value',{})['currency_id']:
            user_pool = self.pool.get("res.users")
            vals['value']['currency_id'] = user_pool.browse(cr, uid, uid).company_id.currency_id.id
        return vals

    def copy(self, cr, uid, ids, default=None, context=None):
        if not default:
            default = {}
        default.update({'check_number': False})
        return super(account_voucher, self).copy(cr, uid, ids, default=default, context=context)

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        """
            Add domain 'allow_check_writing = True' on journal_id field and remove 'widget = selection' on the same
            field because the dynamic domain is not allowed on such widget
        """
        if not context: context = {}
        res = super(account_voucher, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        nodes = doc.xpath("//field[@name='journal_id']")
        if context.get('write_check', False) :
            for node in nodes:
                node.set('domain', "[('type', '=', 'bank'), ('allow_check_writing','=',True)]")
                node.set('widget', '')
            res['arch'] = etree.tostring(doc)
        return res
    def print_check(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        value = {}
        model_data = self.pool.get('ir.model.data')
        check_layout_report = {
             'top' : 'account.print.check.top',
             'middle' : 'account.print.check.middle',
             'bottom' : 'account.print.check.bottom',
         }
        check = self.browse(cr, uid, ids[0], context=context)
        if check.check_number or check.journal_id.use_preprint_check :
            check_layout = check.company_id.check_layout
            value =  {
                 'type': 'ir.actions.report.xml', 
                 'report_name':check_layout_report[check_layout],
                 'datas': {
                         'model':'account.voucher',
                         'id': ids and ids[0] or False,
                         'ids': ids and ids or [],
                         'report_type': 'pdf'
                     },
                 'nodestroy': True
             }
        else:
            form_view = model_data.get_object_reference(cr, uid, 'account_check_writing', 'view_account_check_write')
            value = {
                    'name': _('Print Check'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'account.check.write',
                    'views': [(form_view and form_view[1] or False, 'form'),(False, 'tree')],
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': context,
            }
        return value

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
