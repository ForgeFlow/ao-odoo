# -*- coding: utf-8 -*-
# © 2016 David Dufresne <david.dufresne@savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging


logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to speed up the installation
    of the module on an existing Odoo instance.
    """
    store_field_bom_standard_cost(cr)


def store_field_bom_standard_cost(cr):

    cr.execute("""SELECT column_name
    FROM information_schema.columns
    WHERE table_name='product_template' AND
    column_name='bom_standard_cost'""")
    if not cr.fetchone():
        cr.execute(
            """
            ALTER TABLE product_template ADD COLUMN bom_standard_cost float;
            """)

        logger.info('Computing field bom_standard_cost on product.template')
        # todo: do it from ir_values
        """
            select split_part(res_id, ',', 1) AS col1,
            split_part(res_id, ',', 2) AS col2, value_text
             from ir_property where name = 'standard_price'        
        """
        cr.execute(
            """
                UPDATE product_template
                SET bom_standard_cost = list_price
            """
        )
