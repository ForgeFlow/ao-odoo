# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "HelpDesk Set Reply-To",
    "version": "12.0.1.0.0",
    "author": "Ursa Information Systems, Eficent",
    "license": "AGPL-3",
    "category": "Sales Management",
    "summary": "Sets reply-to in the helpdesk item.",
    "website": "https://www.eficent.com",
    "depends": [
        "mail",
        "crm_helpdesk",
        "fetchmail",
    ],
    "data": [
        "data/crm_helpdesk_config_data.xml",
        "views/crm_helpdesk_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
