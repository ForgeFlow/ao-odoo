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

from openerp.osv import osv
from openerp.osv import fields
from openerp import SUPERUSER_ID

class account_journal(osv.osv):
    _inherit = "account.journal"

    _columns = {
        'allow_check_writing': fields.boolean('Allow Check Writing', help='Check this to be able to write checks using this journal.'),
        'use_preprint_check': fields.boolean('Use Preprinted Checks', help="Check this if your checks already have a number preprinted on them. Otherwise check numbers will be printed on paper."),
        'check_sequence_id': fields.many2one('ir.sequence', 'Check Sequence', help="This field contains the information related to the numbering of the Check of this journal."),
        }

    def create_check_sequence(self, cr, uid, vals, context=None):
        """ 
        Create new no_gap entry sequence for check Journal using given vals.
        """
        val = {
            'name': vals['name'] + " Check Number",
            'implementation':'no_gap',
            'padding': 4,
            'number_increment': 1
        }
        if 'company_id' in vals:
            val['company_id'] = vals['company_id']
        return self.pool.get('ir.sequence').create(cr, uid, val, context)

    def create(self, cr, uid, vals, context=None):
        if not 'check_sequence_id' in vals or not vals['check_sequence_id']  and vals.get('allow_check_writing'):
            # if we have the right to create a journal, we should be able to
            # create it's check number sequence.
            vals.update({'check_sequence_id': self.create_check_sequence(cr, SUPERUSER_ID, vals, context)})
        return super(account_journal, self).create(cr, uid, vals, context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
