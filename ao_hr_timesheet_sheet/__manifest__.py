# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on HR Timesheet Sheet",
    "version": "11.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Human Resources",
    "depends": ["hr_timesheet_sheet"],
    "license": "AGPL-3",
    "data": [
        "security/hr_timesheet_sheet_security.xml",
        "views/account_analytic_line_view.xml",
    ],
    "installable": True,
}
