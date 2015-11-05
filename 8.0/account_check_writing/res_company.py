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

from openerp import models, fields

class res_company(models.Model):
    _inherit = 'res.company'

    check_layout = fields.Selection([
        ('top', 'Check on Top'),
        ('middle', 'Check in middle'),
        ('bottom', 'Check on bottom'),
        ], string='Choose Check layout', default='top',
        help="Check on top is compatible with Quicken, QuickBooks and Microsoft Money. Check in middle is compatible with Peachtree, ACCPAC and DacEasy. Check on bottom is compatible with Peachtree, ACCPAC and DacEasy only")
    credit_section = fields.Boolean(string='Display Credits Separately', help="Invoices and credits will be displayed in their respective section on the check stubs.")
    suppress_unpaid = fields.Boolean(string='Suppress Unpaid Items', help="Do not print unpaid items on the check stubs.")
    multi_stub = fields.Boolean(string='Multi-Pages Check Stub', help="This option allows you to print check details (stub) on multiple pages.")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: