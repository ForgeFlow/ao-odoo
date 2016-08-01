# -*- coding: utf-8 -*-
#########################################################################
#                                                                       #
#                                                                       #
#########################################################################
#                                                                       #
# Copyright (C) 2009-2011  Akretion, Raphaël Valyi, Sébastien Beau, 	#
# Emmanuel Samyn, Benoît Guillot                                        #
#                                                                       #
#This program is free software: you can redistribute it and/or modify   #
#it under the terms of the GNU General Public License as published by   #
#the Free Software Foundation, either version 3 of the License, or      #
#(at your option) any later version.                                    #
#                                                                       #
#This program is distributed in the hope that it will be useful,        #
#but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#GNU General Public License for more details.                           #
#                                                                       #
#You should have received a copy of the GNU General Public License      #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

from openerp import models, fields, api, _

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    claim_id = fields.Many2one('crm.claim', 'Claim')    
    
    @api.model
    def _get_cleanup_fields(self):
        fields = super(account_invoice, self)._get_cleanup_fields()
        fields = fields + ('claim_line_id',)
        return fields
    
    @api.model
    def _refund_cleanup_lines(self, lines):
        new_lines = []
        if self.env.context.get('claim_line_ids') and lines and 'product_id' in lines[0]:#check if is an invoice_line
            for claim_line_id in self.env.context.get('claim_line_ids'):
                claim_info = self.env['claim.line'].read(claim_line_id[1], ['invoice_line_id', 'product_returned_quantity', 'refund_line_id'])
                if not claim_info['refund_line_id']:
                    invoice_line_info = self.env['account.invoice.line'].read(claim_info['invoice_line_id'][0])
                    invoice_line_info['quantity'] = claim_info['product_returned_quantity']
                    invoice_line_info['claim_line_id'] = [claim_line_id[1]]
                    new_lines.append(invoice_line_info)
            if not new_lines:
                #TODO use custom states to show button of this wizard or not instead of raise an error
                raise Warning(_('Error !'), _('A refund has already been created for this claim !'))
            lines = new_lines
        result = super(account_invoice, self)._refund_cleanup_lines(lines)
        return result
    
    @api.model
    def _prepare_refund(self,invoice, date=None, period_id=None, description=None, journal_id=None):
        result = super(account_invoice, self)._prepare_refund(invoice, date=date, period_id=period_id, description=description, journal_id=journal_id)
        if self.env.context.get('claim_id'):
            result['claim_id'] = self.env.context.get('claim_id')
        return result

class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"
    
    @api.model
    def create(self, vals):
        claim_line_id = False
        if vals.get('claim_line_id'):
            claim_line_id = vals['claim_line_id']
            del vals['claim_line_id']
        line_id = super(account_invoice_line, self).create(vals)
        if claim_line_id:
            self.env['claim.line'].write(claim_line_id, {'refund_line_id': line_id})
        return line_id
