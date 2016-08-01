# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Enapps LTD (<http://www.enapps.co.uk>).
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

from openerp import models, fields, api, _
from openerp.addons.decimal_precision import decimal_precision as dp

class account_account(models.Model):
    _name = 'account.account'
    _inherit = 'account.account'

    category_ids = fields.Many2many('account_fstr.category', 'account_fstr_category_account', 'category_id', 'account_id', string='Categories')
    
    @api.multi
    def test_category_list(self, category_ids):
        category_ids = category_ids[0][2]
        warning = {}
        warning_category_names = []
        category_pool = self.env['account_fstr.category']
        for account in self:
#             progenitors = [ctgry.progenitor_id.id for ctgry in account.category_ids]
            progenitors = account.category_ids.mapped('progenitor_id.id')
#             current_category_ids = [ctgry.id for ctgry in account.category_ids]
            current_category_ids = account.category_ids.mapped('id')
            new_categories = list(set(category_ids) - set(current_category_ids))
            new_categories_objs = category_pool.browse(new_categories)
            if len(new_categories_objs) > len(new_categories_objs.mapped('progenitor_id.id')):
                warning.update({
                    'title': 'Alert',
                    'message': "You cant add one account to more than one category within the same repoting template",
                })
                return {'value': {'category_ids': current_category_ids}, 'warning': warning}
            
            for category in new_categories_objs:
                if category.progenitor_id.id in progenitors:
                    warning_category_names.append("%s / %s " % (category.progenitor_id.name, category.name))
                    category_ids.remove(category.id)
                    
        if warning_category_names:
            warning.update({
                'title': 'Alert',
                'message': "Categories %s already exist for current account" % (", ".join(warning_category_names)),
            })
        return {'value': {'category_ids': category_ids}, 'warning': warning}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: