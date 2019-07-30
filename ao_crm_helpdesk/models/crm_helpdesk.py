# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmHelpdesk(models.Model):
    """ Helpdesk Cases """

    _inherit = "crm.helpdesk"

    def _get_default_priority(self):
        if self.partner_id:
            if self.partner_id.helpdesk_default_priority:
                return self.partner_id.helpdesk_default_priority
            else:
                commercial_partner = self.partner_id.commercial_partner_id
                if commercial_partner and \
                        commercial_partner.helpdesk_default_priority:
                    return commercial_partner.helpdesk_default_priority
        return '1'

    priority = fields.Selection(
        default=_get_default_priority
    )

    phone = fields.Char('Phone')

    state = fields.Selection(
        [('draft', 'New'),
         ('open', 'In Progress'),
         ('pending', 'Pending'),
         ('done', 'Closed'),
         ('resolved', 'Resolved'),
         ('cancel', 'Cancelled')], 'Status',
        track_visibility='onchange', index=True,
        help='The status is set to \'Draft\', when a case is created.\
                  \nIf the case is in progress the status is set to \'Open\'.\
                  \nWhen the case is over, the status is set to \'Done\'.\
                  \nIf the case needs to be reviewed then the status is set to'
             ' \'Pending\'.', default='draft')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.priority = self._get_default_priority()

    @api.model
    def message_new(self, msg, custom_values=None):
        """
        When state Resolved and a message is catch, change state to In Progress
        """
        res = super(CrmHelpdesk, self).message_new(
            msg, custom_values=custom_values)
        if self.state == 'resolved':
            self.write({'state': 'open'})
        return res
