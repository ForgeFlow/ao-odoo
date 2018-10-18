# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    manf_country = fields.Many2one(
        comodel_name="res.country", string="Country of Origin",
    )
    scheduleb = fields.Char(
        string="Schedule B #", help="Schedule B number for item",
    )
