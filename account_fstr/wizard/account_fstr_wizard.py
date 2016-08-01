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

from openerp import fields, models, api, _

class account_fstr_wizard(models.TransientModel):

    _name = 'account_fstr.wizard'
    _description = 'Template Print/Preview'
    
    fiscalyear = fields.Many2one('account.fiscalyear', \
                                'Fiscal year', \
                                help='Keep empty for all open fiscal years')
    period_from = fields.Many2one('account.period', 'Start period')
    period_to = fields.Many2one('account.period', 'End period')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                     ('all', 'All Entries'),
                                    ], 'Target Moves', required=True, default='posted')
    root_node = fields.Many2one('account_fstr.category', 'Statement', required=True,)
    hide_zero = fields.Boolean('Hide accounts with a zero balance')
    
    @api.model
    def default_get(self, fields):
        result = super(account_fstr_wizard, self).default_get(fields)
        result['root_node'] = self.env.context.get('active_id', None)
        return result
    
    @api.multi
    def onchange_fiscalyear(self, fiscalyear_id=False):
        res = {}
        res['value'] = {}
        if fiscalyear_id:
            start_period = end_period = False
            self.env.cr.execute('''
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               ORDER BY p.date_start ASC
                               LIMIT 1) AS period_start
                UNION
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.date_start < NOW()
                               ORDER BY p.date_stop DESC
                               LIMIT 1) AS period_stop''', (fiscalyear_id, fiscalyear_id))
            periods = [i[0] for i in self.env.cr.fetchall()]
            if periods and len(periods) > 1:
                start_period = periods[0]
                end_period = periods[1]
            res['value'] = {'period_from': start_period, 'period_to': end_period}
        return res
    
    @api.multi
    def open_window(self):
        """
        Opens chart of Accounts
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of account chart’s IDs
        @return: dictionary of Open account chart window on given fiscalyear and all Entries or posted entries
        """
        period_obj = self.env['account.period']
        fy_obj = self.env['account.fiscalyear']
        
        data = self.read([])[0]
        result = self.env.ref('account_fstr.action_account_fstr_category_tree')
        result = result.read()[0]
        result['periods'] = []
        if data['period_from'] and data['period_to']:
            result['periods'] = period_obj.build_ctx_periods(data['period_from'][0], data['period_to'][0])
        result['context'] = str({'fiscalyear': data['fiscalyear'][0], 'periods': result['periods'], 'state': data['target_move']})
        if data['fiscalyear']:
            fy = fy_obj.browse(data['fiscalyear'][0])
            result['name'] += ':' + fy.read()[0]['code']
        result['domain'] = [('id', '=', data['root_node'][0])]
        return result
    
    @api.multi
    def print_template(self):
        period_obj = self.env['account.period']
        data = self.read([])[0]
        data_obj = self
        datas = {'periods': [], 'ids': self.ids}
        ctx = dict(self.env.context or {})
        if data['period_from'] and data['period_to']:
            ctx['periods'] = period_obj.build_ctx_periods(data['period_from'][0], data['period_to'][0])
        datas['context'] = str({'fiscalyear': data['fiscalyear'], 'periods': datas['periods'], \
                                    'state': data['target_move']})
        datas['period_from'] = data_obj.period_from.name
        datas['period_to'] = data_obj.period_to.name
        datas['fiscalyear'] = data_obj.fiscalyear.name
        ctx['account_fstr_root_node'] = data['root_node']
        ctx['hide_zero'] = data['hide_zero']
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account_fstr.report',
            'datas': datas,
            'context': ctx,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: