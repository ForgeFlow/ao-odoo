# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _get_domain_auto_close_po(self):
        return [
            ("state", "=", "purchase"),
            ("invoice_status", "=", "invoiced"),
            ("qty_to_invoice", "=", 0),
            ("qty_to_receive", "=", 0),
            ("unreconciled", "=", False),
        ]

    @api.model
    def cron_ao_auto_close_purchases(self):
        """Auto-close PO's.
        """
        _logger.info("Start job")
        domain = self._get_domain_auto_close_po()
        completed_pos = self.search(domain)
        completed_pos.write({
            "state": "done",
        })
        _logger.info("Closed %s Purchase Orders" % len(completed_pos))
        return True
