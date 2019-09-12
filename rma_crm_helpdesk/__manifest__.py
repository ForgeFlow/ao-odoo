# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "RMA CRM Helpdesk",
    "summary": "Allows to create RMAs from a Helpesk Ticket, and to track the "
               "relationship between Tickets and RMA Lines.",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    "website": "https://www.eficent.com",
    "category": "RMA",
    "depends": ["rma", "crm_helpdesk"],
    "license": "AGPL-3",
    "data": [
        'security/ir.model.access.csv',
        'views/rma_order_view.xml',
        'views/rma_order_line_view.xml',
        'views/crm_helpdesk_view.xml',
    ],
    'installable': True,
}
