# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tools.translate import _
from odoo import fields, models

_logger = logging.getLogger(__name__)


class BomStructureXlsx(models.AbstractModel):
    _name = 'report.ao_mrp_bom_structure_xlsx.bom_structure_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def print_bom_children(self, ch, sheet, row, level, workbook):
        today = fields.Date.today()
        company = self.env['res.company'].browse(self._context.get(
            'company_id')) or self.env['res.users']._get_company()
        i, j = row, level
        j += 1
        sheet.write(i, 1, '> ' * j)
        sheet.write(i, 2, ch.product_id.default_code or '')
        sheet.write(i, 3, ch.product_id.display_name or '')
        sheet.write(i, 4, ch.product_uom_id._compute_quantity(
            ch.product_qty, ch.product_id.uom_id) or '')
        sheet.write(i, 5, ch.product_id.uom_id.name or '')
        sheet.write(i, 6, ch.bom_id.code or '')
        sheet.write(i, 7, ch.product_id.manufacturer.name or '')
        sheet.write(i, 8, ch.product_id.manufacturer_pref or '')
        empty = workbook.add_format({'bg_color': 'ffcc00'})
        alert = workbook.add_format({'bg_color': 'ff3333'})
        list_prices = []
        for seller in ch.product_id.seller_ids:
            if seller.price:
                if seller.product_uom.category_id.id != ch.product_uom_id.\
                        category_id.id:
                    sheet.write(i, 9, seller.name.name or '')
                    sheet.write(i, 10, seller.product_code or '')
                    sheet.write(i, 11, seller.product_uom.name or '', alert)
                    break
                unit_qty = seller.product_uom._compute_quantity(
                    1.0, ch.product_uom_id, round=False)
                cur_from = seller.currency_id
                cur_to = ch.product_id.currency_id
                price = cur_from._convert(seller.price, cur_to, company, today)
                price_unit = price / unit_qty
                list_prices += [price_unit]
        if list_prices:
            seller_price = min(list_prices)
            list_seller = []
            sellers = 0
            for seller in ch.product_id.seller_ids:
                seller_id = seller.name.id
                if seller.price:
                    if seller.product_uom.category_id.id != ch.product_uom_id.\
                            category_id.id:
                        sheet.write(i, 9, seller.name.name or '')
                        sheet.write(i, 10, seller.product_code or '')
                        sheet.write(i, 11, seller.product_uom.name or '',
                                    alert)
                        break
                    unit_qty = seller.product_uom._compute_quantity(
                        1.0, ch.product_uom_id, round=False)
                    cur_from = seller.currency_id
                    cur_to = ch.product_id.currency_id
                    price = cur_from._convert(
                        seller.price, cur_to, company, today)
                    price_unit = price / unit_qty
                else:
                    price_unit = False
                if price_unit and seller_price == price_unit \
                        and seller_id not in list_seller:
                    list_seller += [seller_id]
                    sheet.write(i, 9, seller.name.name or '')
                    sheet.write(i, 10, seller.product_code or '')
                    uom = ch.product_uom_id.name
                    cur = ch.product_id.currency_id.name
                    uom_cur = workbook.add_format(
                        {'num_format': '#,##0.00 [$' + cur + '/' + uom +
                                       '];-#,##0.00 [$' + cur + '/' + uom +
                                       ']'})
                    curr = workbook.add_format(
                        {'num_format': '#,##0.00 [$' + cur + '];-#,##0.00 [$' +
                                       cur + ']'})
                    sheet.write(i, 11, seller.product_uom.name or '')
                    sheet.write(i, 12, price_unit or '', uom_cur)
                    sheet.write(i, 13, ch.product_qty * price_unit or '',
                                curr)
                    i += 1
                    sellers += 1
            if sellers > 0:
                i -= 1
        else:
            seller_price = False
        i += 1
        childs = 0
        sum_prices = 0.0
        for child in ch.child_line_ids:
            i, price_ch = self.print_bom_children(child, sheet, i, j, workbook)
            cur_from = child.product_id.currency_id
            cur_to = ch.product_id.currency_id
            price_ch = cur_from._convert(
                price_ch, cur_to, company, today)
            sum_prices += price_ch
            childs += 1
        if childs == 0:
            if seller_price:
                sum_prices = ch.product_qty * seller_price
            else:
                sheet.write(i - 1, 12, '', empty)
        j -= 1
        return i, sum_prices

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 11.0'})
        sheet = workbook.add_worksheet(_('BoM Structure'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 2, 20)
        sheet.set_column(3, 3, 40)
        sheet.set_column(4, 5, 20)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 10, 20)
        sheet.set_column(11, 11, 10)
        sheet.set_column(12, 13, 20)
        empty = workbook.add_format({'bg_color': 'ffcc00', 'bold': True})
        alert = workbook.add_format({'bg_color': 'ff3333', 'bold': True})
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
                       _('Distr. UOM'),
                       _('Price per Unit'),
                       _('Price per BoM Qty')
                       ]
        sheet_end = [_('Total BoM Price:')]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        i = 2
        today = fields.Date.today()
        company = self.env['res.company'].browse(self._context.get(
            'company_id')) or self.env['res.users']._get_company()
        for o in objects:
            sheet.write(i, 0, o.product_tmpl_id.name or '', bold)
            sheet.write(i, 1, '', bold)
            sheet.write(i, 2, o.product_id.default_code or '', bold)
            sheet.write(i, 3, o.product_id.name or '', bold)
            sheet.write(i, 4, o.product_qty, bold)
            sheet.write(i, 5, o.product_uom_id.name or '', bold)
            sheet.write(i, 6, o.code or '', bold)
            sheet.write(i, 7, o.product_id.manufacturer.name or '', bold)
            sheet.write(i, 8, o.product_id.manufacturer_pref or '', bold)
            list_prices = []
            for seller in o.product_id.seller_ids:
                if seller.price:
                    if seller.product_uom.category_id.id != o.product_uom.\
                            category_id.id:
                        sheet.write(i, 9, seller.name.name or '', bold)
                        sheet.write(i, 10, seller.product_code or '', bold)
                        sheet.write(i, 11, seller.product_uom.name or '',
                                    alert)
                        break
                    # uom_from = seller.product_uom.id
                    # uom_to = o.product_uom_id.id
                    unit_qty = seller.product_uom._compute_quantity(
                        1.0, o.product_uom_id, round=False)
                    cur_from = seller.currency_id
                    cur_to = o.product_id.currency_id or o.product_tmpl_id.\
                        currency_id
                    price = cur_from._convert(
                        seller.price, cur_to, company, today)
                    price_unit = price / unit_qty
                    list_prices += [price_unit]
            if list_prices:
                seller_price = min(list_prices)
                list_seller = []
                sellers = 0
                for seller in o.product_id.seller_ids:
                    seller_id = seller.name.id
                    if seller.price:
                        if seller.product_uom.category_id.id != o.product_uom.\
                                category_id.id:
                            sheet.write(i, 9, seller.name.name or '', bold)
                            sheet.write(i, 10, seller.product_code or '', bold)
                            sheet.write(i, 11, seller.product_uom.name or '',
                                        alert)
                            break
                        unit_qty = seller.product_uom._compute_quantity(
                            1.0, o.product_uom_id, round=False)
                        cur_from = seller.currency_id
                        cur_to = o.product_id.currency_id or o.\
                            product_tmpl_id.currency_id
                        price = cur_from._convert(
                            seller.price, cur_to, company, today)
                        price_unit = price / unit_qty
                    else:
                        price_unit = False
                    if price_unit and seller_price == price_unit \
                            and seller_id not in list_seller:
                        list_seller += [seller_id]
                        sheet.write(i, 9, seller.name.name or '',
                                    bold)
                        sheet.write(i, 10, seller.product_code or
                                    '', bold)
                        uom = o.product_uom.name
                        cur = o.product_id.currency_id.name or o.\
                            product_tmpl_id.currency_id.name
                        uom_cur_bold = workbook.add_format(
                            {'num_format': '#,##0.00 [$' + cur + '/' + uom +
                                           '];-#,##0.00 [$' + cur + '/' + uom +
                                           ']', 'bold': True})
                        curr_bold = workbook.add_format(
                            {'num_format': '#,##0.00 [$' + cur +
                                           '];-#,##0.00 [$' + cur + ']',
                             'bold': True})
                        sheet.write(i, 11, seller.product_uom.name or '')
                        sheet.write(i, 12, price_unit or '', uom_cur_bold)
                        sheet.write(i, 13, o.product_qty * price_unit or '',
                                    curr_bold)
                        i += 1
                        sellers += 1
                if sellers > 0:
                    i -= 1
            else:
                seller_price = False
            i += 1
            j = 0
            childs = 0
            sum_prices = 0.0
            for ch in o.bom_line_ids:
                i, price_ch = self.print_bom_children(
                    ch, sheet, i, j, workbook)
                cur_from = ch.product_id.currency_id
                cur_to = o.product_id.currency_id or o.product_tmpl_id.\
                    currency_id
                price_ch = cur_from._convert(price_ch, cur_to, company, today)
                sum_prices += price_ch
                childs += 1
            if childs == 0:
                if seller_price:
                    sum_prices = o.product_qty * seller_price
                else:
                    sheet.write(i - 1, 12, '', empty)
            sheet.write_row(i, 12, sheet_end, title_style)
            cur = o.product_id.currency_id.name or o.product_tmpl_id.\
                currency_id.name
            curr_bold = workbook.add_format(
                {'bold': True, 'bg_color': '#FFFFCC', 'bottom': 1,
                 'num_format': '#,##0.00 [$' + cur + '];-#,##0.00 [$' + cur +
                               ']'})
            sheet.write(i, 13, sum_prices, curr_bold)
            i += 1
