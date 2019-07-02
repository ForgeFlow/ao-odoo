# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

__name__ = "Upgrade to 11.0.2.0.0"


def migrate(cr, version):
    """ We want to reopen PO's that we accidentally closed."""
    _logger.info("Starting reopening locked POs that should not be.")
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    pos_to_reopen = env['purchase.order'].search([
        ("state", "=", "done"),
        ("write_date", ">=", "2019-07-01 09:00:00"),
        '|',
        ("pending_qty_to_invoice", "=", True),
        ("pending_qty_to_receive", "=", True),
    ])
    for po in pos_to_reopen:
        _logger.info("Reopening PO %s", po.name)
        po.button_unlock()
    _logger.info("Finalized reopening locked POs that should not be.")
