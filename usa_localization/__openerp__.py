# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    'name': 'United States - Localizations',
    'category': 'Ursa',
    'version': '1.0',
    'summary': "Changes (from Ursa) for users implementing OpenERP in the US.",
    'description':
        """
This module quickly configures OpenERP for the most common needs of the United States market.

URSA RECOMMENDS THIS SHOULD BE THE FIRST MODULE INSTALLED.

Specifically:

1. Accounting: installs the following modules: US Chart of Accounts, Anglo-Saxon Accounting. Sets USD as the default and base currency.

2. Jurisdictional: adds American Samoa, Guam, Northern Mariana Islands, Puerto Rico, United States Minor Outlying Islands and U.S. Virgin Islands as territories (states) of the United States so they can be used in partner addresses.  Removes country from US addresses in reports.

3. International - standardizes country names (ie: "Congo, Democratic Repulic of" is now "DR Congo" and "Afghanistan, Islamic State of" is now "Afghanistan".)

4. Usability - sets the Administrator to belong to the Technical Features group, Technical becomes a top level menu

5. Formatting - makes changes to numeric formatting (comma separated thousands) and dates (no seconds, AM/PM indicator).


OpenERP Version:  7.0

Contact: rcarnes@ursainfosystems.com
        """,
    'author': 'Ursa Information Systems',
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.ursainfosystems.com',
    'depends': [
#                'base','account_anglo_saxon','account_voucher','base_crypt','sale_crm',
#                'stock_no_autopicking','sale_mrp','web_shortcuts','base_calendar',
#                'contacts',
               ],
    'data': [
    ],
    'update_xml': [
        'data/base_data.xml',
        'data/res_country_data.xml',
        'data/base_menu.xml',    
        'data/res.country.state.csv', 
        'data/changed_views.xml',        
        ],
    'installable': False,
    'js' : [
    ],
    'css' : [
    ],
    'qweb' : [
    ],
    'test': [
    ],
    'images': [
        'images/sale_crm_crm_dashboard.png', 'images/crm_dashboard.jpeg','images/leads.jpeg','images/meetings.jpeg','images/opportunities.jpeg','images/outbound_calls.jpeg','images/stages.jpeg',
    ],
}
