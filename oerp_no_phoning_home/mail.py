# -*- coding: utf-8 -*-

from openerp.osv import osv
import logging

_logger = logging.getLogger(__name__)

class publisher_warranty_contract(osv.osv):
    _inherit = 'publisher_warranty.contract'

    def update_notification(self, cr, uid, ids, cron_mode=True,
                            context=None):

        _logger.info("NO More Spying Stuff")

        return True


publisher_warranty_contract()

