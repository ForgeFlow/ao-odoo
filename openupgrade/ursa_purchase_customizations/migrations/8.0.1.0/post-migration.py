# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Akretion
#    (<http://www.akretion.com>).
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

from itertools import groupby

from openerp import pooler, SUPERUSER_ID
from openerp.openupgrade import openupgrade, openupgrade_80


def migrate_location_dest_id(cr):

        openupgrade.logged_query(
            cr,
            '''UPDATE purchase_order_line
            SET location_dest_id = {location_dest_id}
            WHERE {location_dest_id} is not null'''.format(
                location_dest_id=openupgrade.get_legacy_name(
                    'location_dest_id')))


@openupgrade.migrate()
def migrate(cr, version):
    migrate_location_dest_id(cr)
