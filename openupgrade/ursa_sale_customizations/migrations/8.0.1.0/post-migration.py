# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.modules.registry import RegistryManager
from openerp.openupgrade import openupgrade, openupgrade_80
from openerp import SUPERUSER_ID as uid


def migrate_warehouse_id(cr, registry):
    warehouse_obj = registry['stock.warehouse']
    location_obj = registry['stock.location']

    map_locs = {}
    mlocs = []
    warehouse_ids = warehouse_obj.search(
        cr, uid, [])
    for warehouse in warehouse_obj.browse(cr, uid, warehouse_ids):
        # Select all the child locations of this Warehouse
        location_ids = location_obj.search(
            cr, uid,
            [('id', 'child_of', warehouse.view_location_id.id)])
        for location_id in location_ids:
            if location_id not in map_locs.keys():
                map_locs[location_id] = warehouse.id
    for map_loc in map_locs.keys():
        mloc = '(%d, %d)' % (map_loc, map_locs[map_loc])
        mlocs.append(mloc)
    loc_map = ', '.join(mlocs)

    openupgrade.logged_query(
        cr, """
        UPDATE sale_order_line SET warehouse_id = m.warehouse
        FROM (VALUES {loc_map}) AS m (location, warehouse)
        WHERE sale_order_line.{location_src_id} = m.location;
        """.format(
            location_src_id=openupgrade.get_legacy_name(
                    'location_src_id'),
            loc_map=loc_map))


@openupgrade.migrate()
def migrate(cr, version):
    registry = RegistryManager.get(cr.dbname)
    migrate_warehouse_id(cr, registry)
