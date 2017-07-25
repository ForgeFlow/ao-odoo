# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, osv, orm
from openerp.tools import html2plaintext
import re

SUBJECT_NAME = [
    'lulzbot education program inquiry',
    'checkout help',
    'enterprise inquiry'
]


class CrmLead(osv.osv):

    _inherit = "crm.lead"

    def _prepare_message_new_custom_values(self, cr, uid, msg,
                                           custom_values=None, context=None):
        def parse_description(description):
            fields = ['email', 'first & last name']
            _dict = {}
            description = description.lower()
            for line in description.split('\n'):
                for field in fields:
                    if field in line:
                        split_line = line.split(':')
                        if len(split_line) > 1:
                            _dict[field] = line.split(':')[1].strip()
            return _dict
        subject = msg.get('subject', '')
        subject = subject.lower()
        for subj in SUBJECT_NAME:
            if subj in subject:
                if custom_values is None:
                    custom_values = {}
                desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
                _dict = parse_description(desc)
                email_from = re.sub("\s\[\d\]", "", _dict.get('email')).strip()
                contact_name = _dict.get('first & last name').title()
                # Search for an existing partner:
                partner_id = self.pool.get('res.partner').search(cr, uid, [
                    '|', ('name', '=', contact_name),
                    ('email', '=', email_from)], context=context, limit=1)
                vals = {
                    'email_from': email_from,
                    'contact_name': contact_name,
                    'partner_id': partner_id[0] if partner_id else False,
                }
                msg['from'] = _dict.get('email')
                custom_values.update(vals)
                break
        return custom_values, msg

    def message_new(self, cr, uid, msg, custom_values=None, context=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        rec_id = super(CrmLead, self).message_new(
            cr, uid, msg, custom_values=custom_values, context=context)
        if self._name == 'crm.lead':
            custom_values = {}
            model = self._context.get('thread_model') or self._name
            lead = self.env[model]
            custom_values, msg = self._prepare_message_new_custom_values(
                cr, uid, msg, custom_values, context=context)
            lead.write(custom_values)
        return rec_id
