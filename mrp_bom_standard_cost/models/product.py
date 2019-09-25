# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_labor_account_id = fields.Many2one(
        'account.account', 'Labor Account', company_dependent=True,
        domain=[('deprecated', '=', False)],
        help="For service type products that refer to a labor activity "
             "used in the Bill of Materials as part of Non-material costs "
             "needed to build the finished product")

    property_overhead_account_id = fields.Many2one(
        'account.account', 'Overhead Account', company_dependent=True,
        domain=[('deprecated', '=', False)],
        help="For service type products that refer to an overhead cost "
             "used in the Bill of Materials as part of Non-material costs "
             "needed to build the finished product")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_labor_account_id = fields.Many2one(
        'account.account', 'Labor Account', company_dependent=True,
        domain=[('deprecated', '=', False)],
        help="For service type products that refer to a labor activity "
             "used in the Bill of Materials as part of Non-material costs "
             "needed to build the finished product")

    property_overhead_account_id = fields.Many2one(
        'account.account', 'Overhead Account', company_dependent=True,
        domain=[('deprecated', '=', False)],
        help="For service type products that refer to an overhead cost "
             "used in the Bill of Materials as part of Non-material costs "
             "needed to build the finished product")

    @api.multi
    def get_product_accounts(self, fiscal_pos=None):
        """ Add the non material accounts related to product to the result
        of super()
        @return: dictionary which contains all needed information regarding
        labor and overhead accounts and super (income+expense accounts)
        """
        accounts = super(ProductTemplate, self).get_product_accounts(
            fiscal_pos=fiscal_pos)
        accounts.update({
            'labor_account': (self.property_labor_account_id or
                              self.categ_id.property_labor_account_id or
                              False),
            'overhead_account': (self.property_overhead_account_id or
                                 self.categ_id.property_overhead_account_id
                                 or False),
        })
        return accounts

    def get_accounting_data_for_non_material(self, cost_type):
        """ Return the accounts and journal to use to post Journal Entries """
        accounts_data = self.get_product_accounts()
        acc_labor = accounts_data['labor_account'] and accounts_data[
            'labor_account'].id
        acc_overhead = accounts_data['overhead_account'] and accounts_data[
            'overhead_account'].id

        if cost_type == 'labor' and not acc_labor:
            raise UserError(_(
                'Cannot find a labor account for the product %s. You '
                'must define one on the product category.') % (
                self.display_name))
        if cost_type == 'overhead' and not acc_overhead:
            raise UserError(_(
                'Cannot find an overhead account for the product %s. You '
                'must define one on the product category.') % (
                self.display_name))
        journal_id = accounts_data['stock_journal'].id
        return acc_labor, acc_overhead, journal_id
