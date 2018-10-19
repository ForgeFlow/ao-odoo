# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    user_id = fields.Many2one(track_visibility='onchange')

    @api.multi
    def button_open(self):
        """ Opens the Helpdesk Ticket """
        for helpdesk in self:
            if helpdesk.state == 'draft':
                helpdesk.date_open = fields.datetime.now()
            if not helpdesk.user_id or helpdesk.user_id != self.env.user:
                helpdesk.user_id = self.env.uid
            helpdesk.state = 'open'
