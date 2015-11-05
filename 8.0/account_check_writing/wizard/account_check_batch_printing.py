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

from openerp import models, fields, api, _

CHECK_LAYOUT = {
    'top': 'account.print.check.top',
    'middle': 'account.print.check.middle',
    'bottom': 'account.print.check.bottom',
}


class account_check_write(models.TransientModel):
    _name = 'account.check.write'
    _description = 'Print Check in Batch'
    
    @api.model
    def _get_sequence(self, tolerate_noid=False):
        """
        Generic Method to fetch ir.sequence from voucher journal.
        also tolerate the no seuquence condition, if needed e.g. default_get
        """
        voucher_pool = self.env['account.voucher']
        sequence_id = False
        journal_id = voucher_pool.browse(self.env.context['active_id']).journal_id
        if journal_id.check_sequence_id:
            sequence_id = journal_id.check_sequence_id.id
        elif not journal_id and tolerate_noid:
            #if journal has no sequence we can use generic check sequence.
            ref = self.env.ref('account_check_writingseq_check_number')
            sequence_id = ref.id
        else:
            raise Warning(_('Error!'), _("No check number sequence defined for the journal : %s")%(journal_id.name))
        return sequence_id
    
    @api.model
    def _get_next_number(self):
        num_next = False
        if self.env.context.get('active_id') and self.env.context.get('active_model'):
            sequence_id = self._get_sequence(tolerate_noid=True)
            sequence = self.env['ir.sequence'].browse(sequence_id)
            num_next = sequence.number_next
            
        return num_next
    
    check_number = fields.Integer('Check Sequence Number', required=True, help="This is the number of the first check in the batch-print.", default=_get_next_number)
    force_number = fields.Boolean('Overwrite Check Numbers', help="If checked, it will reassign a new check number from given sequence to the check(s) even if check(s) already have a number.")
    force_overwrite = fields.Boolean('Adjust Sequence', help="Use this if the default check number above is different than the next paper check number.\n- If checked, it will consider the check number above as the new default sequence.\n- Uncheck this if you are printing an exceptional batch.", default=True)
    
    
    @api.model
    def _update_sequence(self, new_value, sequence_id):
        sequence_pool = self.env['ir.sequence']
        return sequence_id.write( {'number_next': new_value})
    
    @api.model
    def _check_journal(self, checks):
        journals = [check.journal_id.id for check in checks]
        for check in checks:
            if check.journal_id.type != "bank":
                raise Warning(_("Warning"), _("Cannot perform operation. Voucher Journal type has to be Bank and Cheques."))
        if len(set(journals)) > 1:
            raise Warning(_("Warning"), _("You cannot batch-print checks from different journals in order to respect each journals sequence."))
        states = [check.state for check in checks]
        if 'draft' in states:
            raise Warning(_("Warning"), _("You cannot print draft checks. You have to validate them first."))
        return True

    @api.multi
    def print_check_write(self):
        voucher_pool = self.env['account.voucher']
        ir_sequence_obj = self.env['ir.sequence']
        transient_record = self
        new_value = transient_record.check_number
        voucher_ids = self.env.context.get('active_ids', [])
        checks = voucher_pool.browse(voucher_ids)
        ir_sequence_obj.browse
        self._check_journal(checks)
        sequence = ir_sequence_obj.browse(self._get_sequence(checks[0]))
        old_next_start = sequence.number_next
        self._update_sequence(new_value, sequence)
        requence_rec = sequence.read(['number_next','number_increment'])
        
        new_next_start ,increment =  requence_rec[0]['number_next'], requence_rec[0]['number_increment']
        
        for check in checks:
            new_value = ir_sequence_obj.next_by_id(sequence.id)
            if check.check_number and not transient_record.force_number:
                raise Warning(_('Error!'), _("At least one of the checks in the batch already has a check number. If you want to overwrite their number in this batch-print, select the corresponding checkbox."))
            else:
                check.write({"check_number": new_value, "check_done": True})
                new_next_start += increment
        up_number = new_next_start if transient_record.force_overwrite else old_next_start
        self._update_sequence(up_number, sequence)

        check_layout = voucher_pool.browse(voucher_ids[0]).company_id.check_layout or 'top'
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