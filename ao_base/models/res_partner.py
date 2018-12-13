# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.partner"

    @api.onchange('state_id')
    def onchange_state(self):
        if self.state_id:
            self.country_id = self.state_id.country_id
