# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C)
#    2010 Colin MacMillan - Enapps Ltd.
#    All Rights Reserved
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

from openerp import fields, models, api, _
from openerp.addons.decimal_precision import decimal_precision as dp
from wizard import account_fstr_wizard

class account_fstr_category(models.Model):
    _name = 'account_fstr.category'
    _description = 'Financial Statement template category'
    _order = 'sequence, id'

    @api.depends('account_ids', 'child_id')
    def _compute(self):
        for category_obj in self:
            category_obj.balance = self._compute_balance_for_caregory(category_obj)

    def _compute_balance_for_caregory(self, category_obj):
        result = 0
        if category_obj.state == 'normal':
            for account_obj in category_obj.account_ids:
                result += account_obj.balance
        else:
            for child_category_obj in category_obj.child_id:
                result += self._compute_balance_for_caregory(child_category_obj)
        return result
    
    @api.depends('parent_id')
    def _get_progenitor_id(self):
        for category_obj in self:
            category_obj.progenitor_id = self._get_progenitor_id_in_recurse(category_obj)
    
    def _get_progenitor_id_in_recurse(self, category_obj):
        result = None
        if not (category_obj.parent_id and category_obj.parent_id.id):
            result = category_obj.id
        else:
            result = self._get_progenitor_id_in_recurse(category_obj.parent_id)
        return result

#     def _get_childs(self, cr, uid, ids, context={}):
#         return self.search(cr, uid, [('id', 'child_of', ids)], context=context)

    name = fields.Char(string='Category Title name', required=True, index=True)
    digits_round = fields.Integer(string='Digits round', required=True, default=0)
    company_id = fields.Many2one('res.company', string='Company', ondelete='set null')
    name_end = fields.Char(string='Category End/Total name')
    display_total = fields.Boolean(string='Display End/Total')
    parent_id = fields.Many2one('account_fstr.category', string='Parent node', ondelete='cascade', index=True)
    sequence = fields.Integer(string='Sequence')
    consolidate_total = fields.Boolean(string='Consolidate total', help="Selecting Consolidate total will print this category total as a single summed figure and will not list out each individual account")
    display_heading = fields.Boolean(string='Display title')
    bold_title = fields.Boolean(string='Bold')
    italic_title = fields.Boolean(string='Italic')
    underline_title = fields.Boolean(string='Underline')
    bold_end = fields.Boolean(string='Bold')
    italic_end = fields.Boolean(string='Italic')
    underline_end = fields.Boolean(string='Underline')
    inversed_sign = fields.Boolean(string='Inversed sign')
    child_id = fields.One2many('account_fstr.category', 'parent_id', string='Consolidated Children', index=True)
    account_ids = fields.Many2many('account.account', 'account_fstr_category_account', 'account_id', 'category_id', string='Accounts', index=True)
    indent_title = fields.Integer(string='Indent Title, (pt)', default=10)
    indent_end = fields.Integer(string='Indent End, (pt)', default=10)
    top_spacing_title = fields.Integer(string='Top spacing Title, (pt)', default=0)
    top_spacing_end = fields.Integer(string='Top spacing End, (pt)')
    bottom_spacing_title = fields.Integer(string='Bottom spacing Title, (pt)')
    bottom_spacing_end = fields.Integer(string='Bottom spacing End, (pt)')
    state = fields.Selection([('view', 'View'), ('root', 'Root'), ('normal', 'Normal')], string='Type', index=True, default='normal')
    balance = fields.Float(compute='_compute', digits_compute=dp.get_precision('Account'), string='Balance', store=False)
    printable = fields.Boolean('Printable', help="Select to allow category to display in print list")
    progenitor_id = fields.Many2one('account_fstr.category', compute='_get_progenitor_id',
                                     string='Root',
                                     store=True, index=True)
    
    @api.constrains('parent_id')
    def _check_recursion(self):
        level = 100
        ids = self.ids
        while len(ids):
            self.env.cr.execute('select distinct parent_id from account_fstr_category where id IN %s', (tuple(self.ids),))
            ids = filter(None, map(lambda x:x[0], self.env.cr.fetchall()))
            if not level:
                raise Warning (_('Error!'), _('You cannot create recursive.'))
            level -= 1
    
    @api.multi
    def print_template(self):
        return account_fstr_wizard.account_fstr_wizard.print_template()

    @api.model
    def _get_selected_accounts(self, progenitor_id, current_category_id):
        result = []
        categories = self.search([('progenitor_id', '=', progenitor_id)])
        for category_obj in categories:
            if category_obj.id != current_category_id:
                result.extend([category.id for category in category_obj.account_ids])
        return result
    
    @api.model
    def test_account_list(self, progenitor_id, account_ids):
        warning = {}
        warning_account_names = []
        current_account_ids = []
        all_account_ids_for_template = self._get_selected_accounts(progenitor_id,
                                                                   self.ids)
        updated_account_ids = account_ids[0][2]
        for account_obj in self.env['account.account'].browse(updated_account_ids):
            if not (account_obj.id in all_account_ids_for_template):
                current_account_ids.append(account_obj.id)
            else:
                warning_account_names.append(account_obj.name)
        if warning_account_names:
            warning.update({
                'title': 'Alert',
                'message': "Accounts %s already exist in current template" % (", ".join(warning_account_names)),
            })
        return {'value': {'account_ids': current_account_ids}, 'warning': warning}
    
    @api.multi
    def view_exception_accounts(self):
        account_list = self._get_selected_accounts(self.id, self.ids)
#         model_data_pool = self.env['ir.model.data']
#         model_data_ids = model_data_pool.search([('model', '=', 'ir.ui.view'), ('name', '=', 'view_account_list')])
#         resource_id = model_data_ids.read(fields=['res_id'])[0]['res_id']
        resource_id = self.env.ref('account.view_account_list').id
        return {
            'name': 'Exception Accounts',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(resource_id, 'tree'), ],
            'res_model': 'account.account',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'domain': [('type', '!=', 'view'), ('id', 'not in', account_list)]
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: