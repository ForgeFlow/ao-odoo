# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Buffer(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.depends('lead_days', 'product_id.seller_ids.delay')
    def _compute_dlt(self):
        purchased_buffers = self.filtered(
            lambda r: r.buffer_profile_id.item_type == 'purchased')
        for rec in purchased_buffers:
            rec.dlt = rec.lead_days
        super(Buffer, self - purchased_buffers)._compute_dlt()
