# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields
from odoo.exceptions import AccessError
from odoo.tools.translate import _


class ResUsers(models.Model):
    _inherit = "res.users"

    calendar_allow_ui_edition = fields.Boolean(
        string="Allow in-calendar edition",
        help="When set you can modify the dates of existing calendar events "
             "by moving them in the calendar view.",
        default=True,
        compute='get_calendar_allow_ui_edition',
        inverse='set_calendar_allow_ui_edition'
    )

    @api.multi
    @api.depends('groups_id')
    def get_calendar_allow_ui_edition(self):
        """ Map user membership to boolean field value """
        users = self.env.ref(
            'ao_calendar.group_calendar_allow_ui_edition').users
        for user in self:
            user.calendar_allow_ui_edition = user in users

    @api.multi
    def set_calendar_allow_ui_edition(self):
        """ Map boolean field value to group membership, but checking
        access """
        group = self.env.ref(
            'ao_calendar.group_calendar_allow_ui_edition')
        for user in self:
            if self.env.ref('base.group_no_one') not in user.groups_id:
                raise AccessError(
                    _('The user does not have access to Allow in-calendar '
                      'edition.'))
        if user.calendar_allow_ui_edition:
            self.sudo().write({'groups_id': [(4, group.id)]})
        else:
            self.sudo().write({'groups_id': [(3, group.id)]})

    def __init__(self, pool, cr):
        super(ResUsers, self).__init__(pool, cr)
        self.SELF_READABLE_FIELDS += [
            'calendar_allow_ui_edition']
        self.SELF_WRITEABLE_FIELDS.append('calendar_allow_ui_edition')
