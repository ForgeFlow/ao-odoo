# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from odoo.exceptions import AccessError
from odoo.tools.translate import _


class ResUsers(models.Model):
    _inherit = 'res.users'

    notification_by_email = fields.Boolean(
        string="System notifications by Email",
        default=True,
        help="Uncheck this box if you don't want to receive System"
             "notification in your email.",
        compute='get_notification_by_email',
        inverse='set_notification_by_email'
    )

    @api.multi
    @api.depends('groups_id')
    def get_notification_by_email(self):
        """ Map user membership to boolean field value """
        users = self.env.ref(
            'ao_mail.group_notification_by_email').users
        for user in self:
            user.calendar_allow_ui_edition = user in users

    @api.multi
    def set_notification_by_email(self):
        """ Map boolean field value to group membership, but checking
        access """
        group = self.env.ref(
            'ao_mail.group_notification_by_email')
        for user in self:
            if self.env.ref('base.group_no_one') not in user.groups_id:
                raise AccessError(
                    _('The user does not have access to System notifications '
                      'by Email.'))
        if user.notification_by_email:
            self.sudo().write({'groups_id': [(4, group.id)]})
        else:
            self.sudo().write({'groups_id': [(3, group.id)]})

    def __init__(self, pool, cr):
        super(ResUsers, self).__init__(pool, cr)
        self.SELF_READABLE_FIELDS += [
            'notification_by_email']
        self.SELF_WRITEABLE_FIELDS.append('notification_by_email')
