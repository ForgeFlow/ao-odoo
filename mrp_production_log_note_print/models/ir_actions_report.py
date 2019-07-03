# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        if self.model == 'mrp.production':
            for res_id in res_ids:
                rec = self.env[self.model].browse(res_id)
                doc_name = self.env['ir.model']._get(rec._name).name
                rec.with_context(mail_notrack=True).message_post(
                    body=_('%s printed') % doc_name)
        return super(IrActionsReport, self).render_qweb_pdf(
            res_ids=res_ids, data=data)
