# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, osv, orm
from openerp.tools import html2plaintext


class CrmHelpdesk(osv.osv):

    _inherit = "crm.helpdesk"

    def _prepare_message_new_custom_values(self, cr, uid, msg,
                                           custom_values=None, context=None):
        custom_values = super(
            CrmHelpdesk, self)._prepare_message_new_custom_values(
            cr, uid, msg, custom_values=custom_values, context=context
        )

        def parse_description(description):
            fields = ['email', 'first & last name',
                      'description of the issue']
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
        to = msg.get('to', '')
        subject.lower()
        if subject.contains('Support Inquiry') and to.contains(
                'support@'):
            if custom_values is None:
                custom_values = {}
            desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
            _dict = parse_description(desc)
            name = _dict.get('first & last name')

            vals = {
                'name': _dict.get('first & last name'),
                'email_from': _dict.get('email'),
                'contact_name': name
            }
            msg['from'] = _dict.get('email')
            custom_values.update(vals)
