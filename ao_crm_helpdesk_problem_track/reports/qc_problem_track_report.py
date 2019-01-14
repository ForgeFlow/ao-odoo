# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import tools
from odoo import api, fields, models


class QCProblemReport(models.Model):
    _name = "qc.problem.report"
    _description = "Problem Tracking Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    name = fields.Char('Name', readonly=True)
    date = fields.Datetime('Helpdesk Create Date', readonly=True)
    notes = fields.Text('Notes', readonly=True)
    problem_group_id = fields.Many2one('qc.problem.group', 'Problem Group',
                                       readonly=True)
    color = fields.Integer('Color Index', readonly=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], 'Rating', readonly=True)
    stage_id = fields.Many2one('qc.stage', 'Stage', readonly=True)
    qc_team_id = fields.Many2one('qc.team', 'QC Team', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    crm_helpdesk_count = fields.Integer('Helpdesk Tickets Count',
                                        readonly=True)

    def _select(self):
        select_str = """
             SELECT qcp.id as id,
                    qcp.name as name,
                    qcp.notes as notes,
                    qcp.problem_group_id as problem_group_id,
                    qcp.color as color,
                    qcp.priority as priority,
                    qcp.stage_id as stage_id,
                    qcp.qc_team_id as qc_team_id,
                    qcp.company_id as company_id,
                    count(hpr) as crm_helpdesk_count,
                    chd.date as date
        """
        return select_str

    def _from(self):
        from_str = """
        qc_problem qcp
            left join helpdesk_problem_rel hpr on hpr.qc_problem_id = qcp.id
            left join crm_helpdesk chd on chd.id = hpr.crm_helpdesk_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
            qcp.id,
            chd.date
        """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table,
                    self._select(),
                    self._from(),
                    self._group_by()))
