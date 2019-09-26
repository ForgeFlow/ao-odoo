# Copyright 2019 Odoo, S.A.
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, _
from odoo.tools import float_round


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False,
                 line_id=False, level=False):
        lines = super(ReportBomStructure, self)._get_bom(
            bom_id, product_id, line_qty, line_id, level
        )
        bom = self.env['mrp.bom'].browse(bom_id)
        bom_quantity = line_qty
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        operations = self._get_operation_line(bom.routing_id, float_round(
            bom_quantity / bom.product_qty, precision_rounding=1,
            rounding_method='UP'), 0)
        # We change the price computation and add the material, labor
        # and overhead costs associated to the BoM
        sub_total = product.uom_id._compute_price(
            bom.standard_cost_total, bom.product_uom_id) * bom_quantity
        lines['total'] = sub_total + sum([op['total'] for op in operations])
        lines['materials_cost'] = product.uom_id._compute_price(
            bom.standard_cost_only_material, bom.product_uom_id) * bom_quantity
        lines['labor_cost'] = product.uom_id._compute_price(
            bom.standard_cost_labor, bom.product_uom_id) * bom_quantity
        lines['overhead_cost'] = product.uom_id._compute_price(
            bom.standard_cost_overhead, bom.product_uom_id) * bom_quantity
        lines['total_labor_cost'] = product.uom_id._compute_price(
            bom.standard_total_cost_labor, bom.product_uom_id) * bom_quantity
        lines['total_overhead_cost'] = product.uom_id._compute_price(
            bom.standard_total_cost_overhead,
            bom.product_uom_id) * bom_quantity
        return lines

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components, total = super(ReportBomStructure, self)._get_bom_lines(
            bom, bom_quantity, product, line_id, level
        )
        for component in components:
            component['materials_cost'] = component['prod_cost']
            component['labor_cost'] = False
            component['overhead_cost'] = False
            bom_id = component.get('child_bom', False)
            if bom_id:
                bom = self.env['mrp.bom'].search([('id', '=', bom_id)],
                                                 limit=1)
                component['materials_cost'] = bom.standard_cost_only_material \
                    * component['prod_qty']
                component['labor_cost'] = bom.standard_cost_labor * \
                    component['prod_qty']
                component['overhead_cost'] = bom.standard_cost_overhead * \
                    component['prod_qty']
                component['total'] = bom.standard_cost_total * \
                    component['prod_qty']
        return components, total

    def _get_pdf_line(self, bom_id, product_id=False, qty=1,
                      child_bom_ids=False, unfolded=False):
        # Not very clean to override the method from super class but...
        if not child_bom_ids:
            child_bom_ids = []

        data = self._get_bom(bom_id=bom_id, product_id=product_id,
                             line_qty=qty)

        def get_sub_lines(bom, product_id, line_qty, line_id, level):
            data = self._get_bom(bom_id=bom.id, product_id=product_id,
                                 line_qty=line_qty, line_id=line_id,
                                 level=level)
            bom_lines = data['components']
            lines = []
            for bom_line in bom_lines:
                lines.append({
                    'name': bom_line['prod_name'],
                    'type': 'bom',
                    'quantity': bom_line['prod_qty'],
                    'uom': bom_line['prod_uom'],
                    'prod_cost': bom_line['prod_cost'],
                    'bom_cost': bom_line['total'],
                    'level': bom_line['level'],
                    'code': bom_line['code'],
                    'materials_cost': bom_line['materials_cost'],
                    'labor_cost': bom_line['labor_cost'],
                    'overhead_cost': bom_line['overhead_cost'],
                })
                if bom_line['child_bom'] and (
                        unfolded or bom_line['child_bom'] in child_bom_ids):
                    line = self.env['mrp.bom.line'].browse(bom_line['line_id'])
                    lines += (get_sub_lines(line.child_bom_id, line.product_id,
                                            line.product_qty * data['bom_qty'],
                                            line, level + 1))
            if data['operations']:
                lines.append({
                    'name': _('Operations'),
                    'type': 'operation',
                    'quantity': data['operations_time'],
                    'uom': _('minutes'),
                    'bom_cost': data['operations_cost'],
                    'level': level,
                })
                for operation in data['operations']:
                    if unfolded or 'operation-' + str(bom.id) in child_bom_ids:
                        lines.append({
                            'name': operation['name'],
                            'type': 'operation',
                            'quantity': operation['duration_expected'],
                            'uom': _('minutes'),
                            'bom_cost': operation['total'],
                            'level': level + 1,
                        })
            return lines

        bom = self.env['mrp.bom'].browse(bom_id)
        product = product_id or bom.product_id or \
            bom.product_tmpl_id.product_variant_id
        pdf_lines = get_sub_lines(bom, product, qty, False, 1)
        data['components'] = []
        data['lines'] = pdf_lines
        return data
