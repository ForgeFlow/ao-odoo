# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class CrmHelpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    @api.v7
    def on_change_partner_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value': {'partner_id': False}}
        warning = {}
        title = False
        message = False
        partner = self.pool.get('res.partner').browse(cr, uid, part,
                                                      context=context)
        if partner.helpdesk_warn != 'no-message':
            title = _("Warning for %s") % partner.name
            message = partner.helpdesk_warn_msg
            warning = {
                'title': title,
                'message': message,
            }
            if partner.helpdesk_warn == 'block':
                return {'value': {'partner_id': False}, 'warning': warning}

        result = super(CrmHelpdesk, self).on_change_partner_id(cr, uid, ids,
                                                               part,
                                                               context=context)

        if result.get('warning', False):
            warning['title'] = title and title + ' & ' + result['warning'][
                'title'] or result['warning']['title']
            warning['message'] = message and message + ' ' + result['warning'][
                'message'] or result['warning']['message']

        if warning:
            result['warning'] = warning
        return result
