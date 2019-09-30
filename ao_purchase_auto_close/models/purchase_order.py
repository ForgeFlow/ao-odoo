# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, _

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _get_domain_auto_close_po(self):
        return [
            ("state", "=", "purchase"),
            ("invoice_status", "=", "invoiced"),
            ("pending_qty_to_invoice", "=", False),
            ("pending_qty_to_receive", "=", False),
        ]

    @api.model
    def cron_ao_auto_close_purchases(self):
        """Auto-close PO's.
        """
        _logger.info("Start job")
        domain = self._get_domain_auto_close_po()
        completed_pos = self.search(domain)
        for po in completed_pos:
            po.write(
                {"state": "done"}
            )
            po.with_context(mail_notrack=True).message_post(
                body=_('PO %s has been automatically closed as it has '
                       'been completely invoiced, every product received,'
                       'and has no Goods Received Not Invoiced pending to '
                       'reconcile.') % po.name)
        _logger.info("Closed %s Purchase Orders" % len(completed_pos))
        return True
