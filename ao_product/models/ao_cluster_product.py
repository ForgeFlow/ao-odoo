# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AoClusterProduct(models.Model):
    _inherit = 'product.product'

    bagging_amount = fields.Integer()
    processed = fields.Boolean()
    inserted = fields.Boolean()
    build_reference = fields.Char()
    print_quality = fields.Integer()
    print_time = fields.Float()
    color = fields.Selection([('black', 'Black'),
                              ('green', 'Green'),
                              ('hammer_gray', 'Hammer Gray'),
                              ('ghost_gray', 'Ghost Gray'),
                              ('flexy_black', 'Flexy Black'),
                              ('flexy_green', 'Flexy Green')],)
    is_cluster_product = fields.Boolean('Cluster Product')
