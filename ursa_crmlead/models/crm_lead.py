# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    reply_to = fields.Char(
        string="Reply-To",
        readonly=True,
        compute="_compute_reply_to",
    )

    def _compute_reply_to(self):
        """By default use AO custom `reply to`, optionally you can set
        `reply_to_alias` to follow standard Odoo behavior."""
        default_reply_to = self.env['ir.config_parameter'].sudo().get_param(
            "crm.lead.default.reply.to", default=False)
        ao_fallback_mail = "LulzBot Sales<" + default_reply_to + ">"
        not_standard = self.filtered(lambda r: not r.team_id.reply_to_alias)
        for rec in not_standard:
            rec.reply_to = ao_fallback_mail
        standard = (self - not_standard)
        if standard:
            aliases = self.mapped('team_id')._notify_get_reply_to(default=None)
            for rec in standard:
                rec.reply_to = aliases.get(
                    rec.team_id.id or 0, ao_fallback_mail)

    @api.model
    def _notify_get_reply_to(
            self, default=None, records=None, company=None, doc_names=None,
    ):
        res = super()._notify_get_reply_to(
            default=default, records=records,
            company=company, doc_names=doc_names,
        )
        default_reply_to = self.env['ir.config_parameter'].sudo().get_param(
            "crm.lead.default.reply.to", default=False)
        if not default_reply_to:
            return res
        leads_to_modify = self.filtered(
            lambda r: not r.team_id.reply_to_alias)
        for lead in leads_to_modify:
            res[lead.id] = default_reply_to
        return res
