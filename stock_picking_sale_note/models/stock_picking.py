# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_order_origin = fields.Boolean(
        string="Has sales order",
        compute="_compute_sale_order_origin",
    )
    sale_note = fields.Text(
        string="Sales Order Terms and Conditions",
        compute="_compute_sale_note",
    )

    @api.multi
    @api.depends('origin')
    def _compute_sale_order_origin(self):
        for picking in self:
            if picking.origin:
                sale_obj = self.env['sale.order']
                sale = sale_obj.search([('name', '=', picking.origin)],
                                       limit=1)
                if sale:
                    picking.sale_order_origin = True

    @api.multi
    @api.depends('origin')
    def _compute_sale_note(self):
        for picking in self:
            if picking.origin:
                sale_obj = self.env['sale.order']
                sale = sale_obj.search([('name', '=', picking.origin)],
                                       limit=1)
                if sale:
                    picking.sale_note = sale.note
