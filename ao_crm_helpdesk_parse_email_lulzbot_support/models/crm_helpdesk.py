# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, models
from odoo.tools import html2plaintext
import re
import logging

_logger = logging.getLogger(__name__)

EMAIL_PATTERN = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    @api.model
    def _prepare_message_new_custom_values(self, msg, custom_values=None):
        custom_values, msg = super(
            CrmHelpdesk, self)._prepare_message_new_custom_values(
                msg, custom_values=custom_values)

        def parse_description(description):
            _dict = {}
            description = description.lower()
            for line in description.split('\n'):
                if 'first & last name' in line:
                    split_line = line.split(':')
                    if len(split_line) > 1:
                        _dict['first & last name'] = line.split(':')[1].strip()
                elif 'email' in line:
                    pattern = re.compile(EMAIL_PATTERN)
                    result = pattern.match(line.split(':')[1].strip())
                    try:
                        _dict['email'] = result.group()
                    except AttributeError:
                        _logger.warning(
                            'Parsing email error for lulzbot webform: %s'
                            % description)
                        _dict['email'] = 'Not found'
            return _dict
        subject = msg.get('subject', '')
        subject = subject.lower()
        keyphrase = self.env['ir.config_parameter'].sudo().get_param(
            'crm.helpdesk.parse.email.keyphrase', default=False)
        if keyphrase and keyphrase in subject:
            if custom_values is None:
                custom_values = {}
            desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
            _dict = parse_description(desc)
            contact_name = False
            email_from = False
            if _dict.get('email'):
                email_from = re.sub(
                    r'\s\[\d\]', '', _dict.get('email')).strip()
            if _dict.get('first & last name'):
                contact_name = _dict.get('first & last name').title()
            # Search for an existing partner:
            if email_from:
                partner_id = self.env['res.partner'].search([
                    ('email', '=', email_from)], limit=1)
            elif contact_name:
                partner_id = self.env['res.partner'].search([
                    ('name', '=', contact_name)], limit=1)
            else:
                partner_id = False
            vals = {
                'email_from': email_from,
                'contact_name': contact_name,
                'partner_id': partner_id.id if partner_id else False,
            }
            # Check if partner has default helpdesk ticket priority or has
            # commercial partner with default helpdesk ticket priority
            if partner_id:
                default_priority = partner_id.helpdesk_default_priority
                commercial_partner = partner_id.commercial_partner_id
                if default_priority:
                    vals.update({
                        'priority': default_priority,
                    })
                elif commercial_partner and commercial_partner.\
                        helpdesk_default_priority:
                    vals.update({
                        'priority':
                            commercial_partner.helpdesk_default_priority,
                    })
            msg['from'] = _dict.get('email')
            custom_values.update(vals)
        return custom_values, msg
