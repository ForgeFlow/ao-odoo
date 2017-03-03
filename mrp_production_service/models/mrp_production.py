# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.model
    def _prepare_service_procurement(self, line):
        location = line.production_id.location_src_id
        return {
            'name': '%s for %s' % (line.product_id.name,
                                  line.production_id.name),
            'origin': line.production_id.name,
            'company_id': line.production_id.company_id.id,
            'date_planned': line.production_id.date_planned,
            'product_id': line.product_id.id,
            'product_qty': line.product_qty,
            'product_uom': line.product_uom.id,
            'location_id': location.id,
            'warehouse_id': location.get_warehouse(location)
        }

    @api.model
    def _create_service_procurement(self, line):
        data = self._prepare_service_procurement(line)
        return self.env['procurement.order'].create(data)

    @api.multi
    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        for production in self:
            for line in production.product_lines:
                if line.product_id.type == 'service':
                    proc = self._create_service_procurement(line)
                    proc.run()
        return res
