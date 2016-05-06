# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
from openupgradelib import openupgrade
_logger = logging.getLogger(__name__)


column_renames = {
    'purchase_order_line': [
        ('location_dest_id', None),
    ],
}


def create_purchase_order_line_fields(cr):
    """ This function creates new purchase order line fields
    """
    _logger.info("Fast creation of the field "
                 "purchase_order_line.location_dest_id")
    cr.execute("""
        ALTER TABLE purchase_order_line
        ADD COLUMN "location_dest_id" integer""")


@openupgrade.migrate()
def migrate(cr, version):
    openupgrade.rename_columns(cr, column_renames)
    create_purchase_order_line_fields(cr)
