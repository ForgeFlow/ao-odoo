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
from openerp.tools.translate import _

CHECK_LAYOUT = {
    'top': 'account.print.check.top',
    'middle': 'account.print.check.middle',
    'bottom': 'account.print.check.bottom',
}


class account_check_write(osv.TransientModel):

    _name = 'account.check.write'
    _description = 'Print Check in Batch'

    _columns = {
        'check_number': fields.integer('Check Sequence Number', required=True, help="This is the number of the first check in the batch-print."),
        'force_number': fields.boolean('Overwrite Check Numbers', help="If checked, it will reassign a new check number from given sequence to the check(s) even if check(s) already have a number."),
        'force_overwrite': fields.boolean('Adjust Sequence', help="Use this if the default check number above is different than the next paper check number.\n- If checked, it will consider the check number above as the new default sequence.\n- Uncheck this if you are printing an exceptional batch."),
    }

    def _get_sequence(self, cr, uid, ids, tolerate_noid=False, context=None):
        """
        Generic Method to fetch ir.sequence from voucher journal.
        also tolerate the no seuquence condition, if needed e.g. default_get
        """
        voucher_pool = self.pool.get('account.voucher')
        sequence_id = False
        journal_id = voucher_pool.browse(cr, uid, context['active_id'], context=context).journal_id
        if journal_id.check_sequence_id:
            sequence_id = journal_id.check_sequence_id.id
        elif not journal_id and tolerate_noid:
            #if journal has no sequence we can use generic check sequence.
            ref, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_check_writing', 'seq_check_number')
        else:
            raise osv.except_osv(_('Error!'), _("No check number sequence defined for the journal : %s")%(journal_id.name))
        return sequence_id

    def _get_next_number(self, cr, uid, context=None):
        num_next = False
        if context == None:
            context = {}
        if context.get('active_id') and context.get('active_model'):
            sequence_id = self._get_sequence(cr, uid, context.get('active_id'), tolerate_noid=True, context=context)
            num_next = self.pool.get('ir.sequence').read(cr, uid, sequence_id, ['number_next'])['number_next']
        return num_next

    _defaults = {
        'check_number': _get_next_number,
        'force_overwrite': True,
    }

    def _update_sequence(self, cr, uid, new_value, sequence_id, context=None):
        sequence_pool = self.pool.get('ir.sequence')
        return sequence_pool.write(cr, uid, sequence_id, {'number_next': new_value})

    def _check_journal(self, cr, uid, checks, context=None):
        journals = [check.journal_id.id for check in checks]
        for check in checks:
            if check.journal_id.type != "bank":
                raise osv.except_osv(_("Warning"), _("Cannot perform operation. Voucher Journal type has to be Bank and Cheques."))
        if len(set(journals)) > 1:
            raise osv.except_osv(_("Warning"), _("You cannot batch-print checks from different journals in order to respect each journals sequence."))
        states = [check.state for check in checks]
        if "draft" in states:
            raise osv.except_osv(_("Warning"), _("You cannot print draft checks. You have to validate them first."))
        return True

    def print_check_write(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_pool = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')
        transient_record = self.browse(cr, uid, ids[0], context=context)
        new_value = transient_record.check_number
        voucher_ids = context.get('active_ids', [])
        checks = voucher_pool.browse(cr, uid, voucher_ids, context=context)
        self._check_journal(cr, uid, checks, context)
        sequence = self._get_sequence(cr, uid, checks[0].id, context=context)
        old_next_start = self.pool.get('ir.sequence').read(cr, uid, sequence, ['number_next'], context)['number_next']
        self._update_sequence(cr, uid, new_value, sequence, context=context)
        requence_rec = self.pool.get('ir.sequence').read(cr, uid, sequence, ['number_next','number_increment'],context=context)
        new_next_start ,increment =  requence_rec['number_next'], requence_rec['number_increment']
        for check in checks:
            new_value = ir_sequence_obj.next_by_id(cr, uid, sequence, context)
            if check.check_number and not transient_record.force_number:
                raise osv.except_osv(_('Error!'), _("At least one of the checks in the batch already has a check number. If you want to overwrite their number in this batch-print, select the corresponding checkbox."))
            else:
                voucher_pool.write(cr, uid, [check.id], {"check_number": new_value, "check_done": True}, context=context)
                new_next_start += increment
        up_number = new_next_start if transient_record.force_overwrite else old_next_start
        self._update_sequence(cr, uid, up_number, sequence, context=context)

        check_layout = voucher_pool.browse(cr, uid, voucher_ids[0], context=context).company_id.check_layout or 'top'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': CHECK_LAYOUT[check_layout],
            'datas': {
                'model': 'account.voucher',
                'ids': voucher_ids,
                'report_type': 'pdf'
            },
            'nodestroy': True
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
