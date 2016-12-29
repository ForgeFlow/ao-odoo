# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services, S.L.
#   (<http://www.eficent.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging


logger = logging.getLogger(__name__)


def compute_account_move_line_stored_invoice_id(cr):
    logger.info('Computing field stored_invoice_id on account.move.line')

    cr.execute(
        """
        UPDATE account_move_line aml
        SET stored_invoice_id = inv.id
        FROM account_move AS am, account_invoice AS inv
        WHERE am.id = aml.move_id
        AND am.id = inv.move_id
        """
    )


def compute_account_move_line_invoice_user_id(cr):
    logger.info('Computing field invoice_user_id on account.move.line')

    cr.execute(
        """
        UPDATE account_move_line aml
        SET invoice_user_id = inv.user_id
        FROM account_invoice AS inv
        WHERE aml.stored_invoice_id = inv.id
        """
    )


def migrate(cr, version):
    if not version:
        return
    compute_account_move_line_stored_invoice_id(cr)
    compute_account_move_line_invoice_user_id(cr)
