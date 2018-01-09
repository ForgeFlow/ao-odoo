# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models, _


class ReportMrpOrder(models.AbstractModel):
    _name = 'report.mrp.report_mrporder'

    @api.multi
    def render_html(self, data=None):
        mo_ids = self.env['mrp.production'].browse(self.ids)
        message = _("<i>Production Order</i> printed by %s" %
                    self.env.user.name)
        mo_ids.message_post(message, message_type='comment')
        values = {
            'doc_model': 'mrp.production',
            'doc_ids': mo_ids.ids,
            'docs': mo_ids
        }
        return self.env['report'].render('mrp.report_mrporder', values)


class ReportAoMrpOrder(models.AbstractModel):
    _name = 'report.ao_mrp.ao_report_mrporder'

    @api.multi
    def render_html(self, data=None):
        mo_ids = self.env['mrp.production'].browse(self.ids)
        message = _("<i>Production Order (AO)</i> printed by %s" %
                    self.env.user.name)
        mo_ids.message_post(message, message_type='comment')
        values = {
            'doc_model': 'mrp.production',
            'doc_ids': mo_ids.ids,
            'docs': mo_ids
        }
        return self.env['report'].render('ao_mrp.ao_report_mrporder', values)
