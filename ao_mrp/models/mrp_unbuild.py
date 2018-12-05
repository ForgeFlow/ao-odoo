# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpUnbuild(models.Model):
    _inherit = "mrp.unbuild"

    @api.onchange('mo_id')
    def onchange_mo_id(self):
        super(MrpUnbuild, self).onchange_mo_id()
        if self.mo_id:
            self.location_dest_id = self.mo_id.location_dest_id
            self.location_id = self.mo_id.location_src_id
