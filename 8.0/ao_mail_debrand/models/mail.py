# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models, tools


class MailNotification(models.Model):
    _inherit = "mail.notification"

    @api.model
    def get_signature_footer(self, user_id, res_model=None, res_id=None,
                              user_signature=True):
        return self.with_context(
            skip_signature_company=True)._get_signature_footer(
            user_id, res_model=res_model, res_id=res_id,
            user_signature=user_signature)
