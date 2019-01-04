# Copyright 2017 Eficent Business and IT Consulting Services S.L.
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

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.priority = self._get_default_priority()
