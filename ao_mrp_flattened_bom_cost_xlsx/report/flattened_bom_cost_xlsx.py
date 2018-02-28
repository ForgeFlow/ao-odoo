# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openerp.report import report_sxw
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    _logger.debug("report_xlsx not installed, Excel export non functional")

    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass


class FlattenedBomXlsx(ReportXlsx):

    def print_flattened_bom_lines(self, bom, requirements, sheet, row, workbook):
        dollars = workbook.add_format({'num_format': '$#,##0.00'})
        i = row + 1
        for product, total_qty in requirements.iteritems():
            sheet.write(i, 1, product.default_code or '')
            sheet.write(i, 2, product.display_name or '')
            sheet.write(i, 3, total_qty or 0.0)
            sheet.write(i, 4, product.uom_id.name or '')
            sheet.write(i, 5, product.code or '')
            sheet.write(i, 6, product.standard_price or '', dollars)
            sheet.write(i, 7, total_qty * product.standard_price or '', dollars)
            i += 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from openerp 10.0'})
        sheet = workbook.add_worksheet(_('Flattened BOM'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 2, 20)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 6, 20)
        bold = workbook.add_format({'bold': True})
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})
        sheet_title = [_('BOM Name'),
                       _('Product Reference'),
                       _('Product Name'),
                       _('Quantity'),
                       _('Unit of Measure'),
                       _('Reference'),
                       _('Unit Cost'),
                       _('Total Cost')
                       ]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        i = 2

        for o in objects:
            totals = o._get_flattened_totals2()
            sheet.write(i, 0, o.product_tmpl_id.name or '', bold)
            sheet.write(i, 1, o.code or '', bold)
            sheet.write(i, 2, o.display_name or '', bold)
            sheet.write(i, 3, 1, bold)
            sheet.write(i, 4, o.product_uom.name or '', bold)
            sheet.write(i, 5, o.code or '', bold)
            i = self.print_flattened_bom_lines(o, totals, sheet, i, workbook)


FlattenedBomXlsx('report.flattened.bom.xlsx', 'mrp.bom',
                 parser=report_sxw.rml_parse)
