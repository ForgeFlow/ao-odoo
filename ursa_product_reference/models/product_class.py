# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductClass(models.Model):
    _name = "product.class"
    _description = "Product Internal Classification"

    code = fields.Char(string="Code", help="Product Classification Code")
    name = fields.Char(string="Name", help="Product Classification Name")
    parent_id = fields.Many2one("product.class", string="Parent Category")
    sequence_no = fields.Integer(
        string="Next number", default=1,
        help="Sequence Number",
    )
