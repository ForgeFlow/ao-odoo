# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models, _
from openerp.exceptions import AccessError


class CrmHelpdesk(models.Model):

    _inherit = "crm.helpdesk"

    @api.multi
    def message_get_suggested_recipients(self):
        recipients = super(
            CrmHelpdesk, self).message_get_suggested_recipients()
        try:
            for helpdesk in self:
                if helpdesk.partner_id:
                    helpdesk._message_add_suggested_recipient(
                        recipients, partner=helpdesk.partner_id,
                        reason=_('Partner'))
                elif helpdesk.email_from:
                    helpdesk._message_add_suggested_recipient(
                        recipients, email=helpdesk.email_from,
                        reason=_('Partner Email'))
        except AccessError:
            # no read access rights -> just ignore suggested
            # recipients because this imply modifying followers
            pass
        return recipients
