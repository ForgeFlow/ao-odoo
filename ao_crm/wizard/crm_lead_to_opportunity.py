# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Lead2OpportunityPartner(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'

    @api.model
    def default_get(self, fields):
        result = super(Lead2OpportunityPartner, self).default_get(fields)
        # Force Convert Action to be Convert to opportunity as default always
        if 'name' in result:
            result['name'] = 'convert'
        return result
