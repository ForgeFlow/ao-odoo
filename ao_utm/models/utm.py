# Copyright 2019 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class UtmMixin(models.AbstractModel):
    _inherit = 'utm.mixin'

    source_id = fields.Many2one('utm.source', 'Source',
                                help="The platform where the lead originates.")
    medium_id = fields.Many2one('utm.medium', 'Medium', oldname='channel_id',
                                help="The type of source.")
