# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade
_logger = logging.getLogger(__name__)


column_renames = {
    'sale_order_line': [
        ('location_src_id', None),
    ],
}


def create_sale_order_line_fields(cr):
    """ This function creates new sales order line fields
    """
    _logger.info("Fast creation of the field "
                 "sale_order_line.warehouse_id")
    cr.execute("""
        ALTER TABLE sale_order_line
        ADD COLUMN "warehouse_id" integer""")


@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_columns(cr, column_renames)
    create_sale_order_line_fields(cr)
