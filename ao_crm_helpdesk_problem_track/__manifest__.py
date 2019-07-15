# Copyright 2017-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on crm helpdesk (problem tracking)",
    "version": "12.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "CRM",
    "depends": ["crm_helpdesk", "quality_control_issue"],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/crm_helpdesk_view.xml",
        "views/qc_problem_track_view.xml",
        "reports/qc_problem_track_views.xml",
    ],
    "installable": True,
}
