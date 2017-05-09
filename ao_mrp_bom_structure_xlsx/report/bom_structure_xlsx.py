# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from openerp.tools.translate import _
from openerp.addons.mrp.report.bom_structure import bom_structure

_logger = logging.getLogger(__name__)

try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    _logger.debug("report_xlsx not installed, Excel export non functional")

    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass


class BomStructureXlsx(ReportXlsx):

    def print_bom_children(self, ch, sheet, row, level, workbook):
        i, j = row, level
        j += 1
        sheet.write(i, 1, '> '*j)
        sheet.write(i, 2, ch.product_id.default_code or '')
        sheet.write(i, 3, ch.product_id.display_name or '')
        sheet.write(i, 4, ch.product_qty)
        sheet.write(i, 5, ch.product_uom.name or '')
        sheet.write(i, 6, ch.bom_id.code or '')
        sheet.write(i, 7, ch.product_id.manufacturer.name or '')
        sheet.write(i, 8, ch.product_id.manufacturer_pref or '')
        childs = 0
        for seller in ch.product_id.seller_ids:
            sheet.write(i, 9, seller.name.name or '')
            sheet.write(i, 10, seller.product_code or '')
            cur = seller.currency_id.name
            curr = workbook.add_format({'num_format': '#,##0.00 [$' + cur +
                                                      '];-#,##0.00 [$' + cur +
                                                      ']'})
            sheet.write(i, 11, seller.min_qty or '')
            sheet.write(i, 12, seller.product_uom.name or '')
            sheet.write(i, 13, seller.price or '', curr)
            sheet.write(i, 14, seller.min_qty * seller.price or '', curr)
            i += 1
            childs += 1
        if childs > 0:
            i -= 1
        i += 1
        for child in ch.child_line_ids:
            i = self.print_bom_children(child, sheet, i, j, workbook)
        j -= 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 9.0'})
        sheet = workbook.add_worksheet(_('BoM Structure'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 2, 20)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 5, 20)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 9, 20)
        sheet.set_column(10, 10, 15)
        sheet.set_column(11, 12, 10)
        sheet.set_column(13, 13, 15)
        sheet.set_column(14, 14, 20)
        bold = workbook.add_format({'bold': True})
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})
        sheet_title = [_('BoM Name'),
                       _('Level'),
                       _('Product Reference'),
                       _('Product Name'),
                       _('Quantity'),
                       _('Unit of Measure'),
                       _('BoM Reference'),
                       _('Manufacturer'),
                       _('Manufacturer Ref.'),
                       _('Distributor'),
                       _('Distributor Ref.'),
                       _('Qty per Unit'),
                       _('UOM'),
                       _('Price per Unit'),
                       _('Total Price per Unit')
                       ]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        i = 2
        for o in objects:
            sheet.write(i, 0, o.product_tmpl_id.name or '', bold)
            sheet.write(i, 1, '', bold)
            sheet.write(i, 2, o.product_id.default_code or '', bold)
            sheet.write(i, 3, o.product_id.name or '', bold)
            sheet.write(i, 4, o.product_qty, bold)
            sheet.write(i, 5, o.product_uom.name or '', bold)
            sheet.write(i, 6, o.code or '', bold)
            sheet.write(i, 7, o.product_id.manufacturer.name or '', bold)
            sheet.write(i, 8, o.product_id.manufacturer_pref or '', bold)
            childs = 0
            for seller in o.product_id.seller_ids:
                sheet.write(i, 9, seller.name.name or '',
                            bold)
                sheet.write(i, 10, seller.product_code or
                            '', bold)
                cur = seller.currency_id.name
                curr_bold = workbook.add_format(
                    {'bold': True, 'num_format': '#,##0.00 [$' + cur +
                                                 '];-#,##0.00 [$' + cur + ']'})
                sheet.write(i, 11, seller.min_qty or '')
                sheet.write(i, 12, seller.product_uom.name or '')
                sheet.write(i, 13, seller.price or '', curr_bold)
                sheet.write(i, 14, seller.min_qty * seller.price or '',
                            curr_bold)
                i += 1
                childs += 1
            if childs > 0:
                i -= 1
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_bom_children(ch, sheet, i, j, workbook)


BomStructureXlsx('report.ao.bom.structure.xlsx', 'mrp.bom',
                  parser=bom_structure)
