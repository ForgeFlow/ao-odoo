# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class RmaOperation(models.Model):
    _inherit = 'rma.operation'

    repair_type_id = fields.Many2one('mrp.repair.type')
