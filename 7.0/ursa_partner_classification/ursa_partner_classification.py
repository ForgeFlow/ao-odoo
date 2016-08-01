# -*- coding: utf-8 -*-
##############################################################################
#
#    Ursa Information Systems
#    Author: Balaji Kannan
#    Copyright (C) 2013 (<http://www.ursainfosystems.com>).
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

from osv import fields, osv
from tools.translate import _

class res_partner_classification(osv.osv):
    _inherit = 'res.partner'

    def _get_selection(self, cr, uid, context={}):
        obj = self.pool.get('res.partner.classification')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['name', 'code'], context)
        res = [(r['code'], r['code'] + " - " + r['name']) for r in res]

        return res
    
    _columns = {
        'class_code': fields.selection(_get_selection,'Classification'),
	}
    
res_partner_classification()


class ursa_partner_classification(osv.osv):
    
    _name = "res.partner.classification"
    _description = "Partner Classification"
    _columns = {
	'code' : fields.char('Code', size=16, required=False, help='Partner Classification Code'),
	'name' : fields.text('Name', size=64, required=False, help='Partner Classification Description')
    }
    
    _sql_constraints = [('code', 'UNIQUE(code)', 'Cannot have duplicate Classification Code')]
    
ursa_partner_classification()
