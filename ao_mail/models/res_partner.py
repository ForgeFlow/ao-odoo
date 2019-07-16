# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _notify(self, message, rdata, record, force_send=False,
                send_after_commit=True, model_description=False,
                mail_auto_delete=True):
        if message.message_type == 'notification':
            notif_partners = self.filtered(
                lambda partner: partner.mapped(
                    'user_ids.notification_by_email'))
        else:
            notif_partners = self
        return super(Partner, notif_partners)._notify(
            message, rdata, record, force_send=force_send,
            send_after_commit=send_after_commit,
            model_description=model_description,
            mail_auto_delete=mail_auto_delete,
        )
