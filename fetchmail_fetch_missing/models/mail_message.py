# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
#           <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class Message(models.Model):

    _inherit = "mail.message"

    @api.multi
    def unlink(self):
        for rec in self:
            self.env['mail.message.trash'].create({
                'message_id': rec.message_id,
            })
        return super(Message, self).unlink()
