# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, SUPERUSER_ID
from odoo.tools import pycompat, mail


class Lead(models.Model):
    _inherit = 'crm.lead'
    _order = 'id DESC'

    understanding_of_need = fields.Text('Understanding of Need')
    understanding_of_impact = fields.Text('Understanding of Impact')
    buying_process = fields.Text('Buying Process')

    stage_id = fields.Many2one(
        'crm.stage', string='Stage',
        domain="['&', ('team_ids', '=', team_id), '|', "
               "('type', '=', type), ('type', '=', 'both')]",
        group_expand='_read_group_stage_ids')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # We completely override the logic here
        super(Lead, self)._read_group_stage_ids(stages, domain, order)
        team_id = self._context.get('default_team_id')
        if team_id:
            search_domain = ['|', ('id', 'in', stages.ids), '|',
                             ('team_ids', '=', False),
                             ('team_ids', 'in', [team_id])]
        else:
            search_domain = ['|', ('id', 'in', stages.ids),
                             ('team_ids', '=', False)]

        # perform search
        stage_ids = stages._search(search_domain,
                                   order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _stage_find(self, team_id=False, domain=None, order='sequence'):
        # We completely override the logic here
        super(Lead, self)._stage_find(
            team_id=team_id, domain=domain, order=order)
        ctx_type = self.env.context.get('default_type')
        types = ['both']
        if ctx_type:
            types += [ctx_type]
        # check whether we should try to add a condition on type
        avoid_add_type_term = any([
            term for term in domain if len(term) == 3 if term[0] == 'lead_type'
        ])
        # collect all team_ids by adding given one,
        # and the ones related to the current leads
        team_ids = set()
        if team_id:
            team_ids.add(team_id)
        for lead in self:
            if lead.team_id:
                team_ids.add(lead.team_id.id)
        # OR all team_ids
        search_domain = []
        if team_ids:
            search_domain += [('|')] * (len(team_ids) - 1)
            for team_id in team_ids:
                search_domain.append(('team_ids', '=', team_id))
        # AND with cases types
        if not avoid_add_type_term:
            search_domain.append(('lead_type', 'in', types))
        # AND with the domain in parameter
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        return self.env['crm.stage'].search(
            search_domain, order=order, limit=1)

    @api.multi
    def message_post_with_view(self, views_or_xmlid, **kwargs):
        if isinstance(views_or_xmlid, pycompat.string_types):
            if views_or_xmlid == 'mail.message_user_assigned':
                views_or_xmlid = 'ao_crm.message_user_assigned_lead'
        super(Lead, self).message_post_with_view(views_or_xmlid, **kwargs)
        return

    @api.multi
    def message_post_with_template(self, template_id, **kwargs):
        if kwargs.get('body'):
            kwargs['body'] = mail.html_sanitize(kwargs.get('body'))
        return super(Lead, self).message_post_with_template(
            template_id, **kwargs)
