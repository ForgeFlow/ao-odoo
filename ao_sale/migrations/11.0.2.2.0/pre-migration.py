# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


def store_qty_to_deliver(cr):

    cr.execute("""SELECT column_name
    FROM information_schema.columns
    WHERE table_name='sale_order_line' AND
    column_name='qty_to_deliver'""")
    if not cr.fetchone():
        cr.execute(
            """
            ALTER TABLE sale_order_line ADD COLUMN qty_to_deliver float;
            """)

    logger.info('Computing field qty_to_deliver on sale.order.line')

    cr.execute(
        """
        UPDATE sale_order_line sol
        SET qty_to_deliver = product_uom_qty-qty_delivered
        """
    )
    cr.execute(
        """
        UPDATE sale_order_line sol
        SET qty_to_deliver = 0
        WHERE sol.product_id in (
        SELECT pp.id from product_product pp
        INNER JOIN product_template pt ON pp.product_tmpl_id = pt.id
        WHERE NOT (pt.invoice_policy = 'delivery'
        AND pt.service_type = 'manual')
        AND pt.type = 'service')
        """
    )


def migrate(cr, version):
    store_qty_to_deliver(cr)
