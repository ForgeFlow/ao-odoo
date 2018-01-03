# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.multi
    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        if 'active' in vals:
            self.mapped('partner_id').write({'active': vals.get('active')})
        return res
