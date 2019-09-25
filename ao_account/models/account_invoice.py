# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# Copyright 2019 Aleph Objects, Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        return super(
            AccountInvoice, self.with_context(
                mail_auto_subscribe_no_notify=True)).create(vals)

    @api.multi
    def write(self, vals):
        return super(
            AccountInvoice, self.with_context(
                mail_auto_subscribe_no_notify=True)).write(vals)

    def _get_partner_bank_id(self, company_id):
        super(AccountInvoice, self)._get_partner_bank_id(company_id)
        return False
