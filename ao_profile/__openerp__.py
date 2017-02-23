# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name' : 'AO Profile',
    'version': '9.0.1.0.0',
    'author': 'Aleph Objects Inc.',
    'summary': 'Contains the modules used by AO',
    'website': 'http://www.eficent.com',
    'category': 'Customizations',
    'depends': [
        # Odoo standard
        'account_asset',
        # 'analytic_contract_hr_expense', -- deprecated
        'crm',
        'mail',
        'account_voucher',
        'point_of_sale',
        'project',
        'note',
        'project_issue',
        'account_accountant',
        'sale',
        'stock',
        'stock_account',
        'mrp',
        'purchase',
        'hr',
        'hr_timesheet',
        'hr_timesheet_sheet',
        'hr_holidays',
        'hr_expense',
        'hr_payroll',
        'account',
        #'account_analytic_default', -- deprecated
        #'account_analytic_plans', -- deprecated
        'account_budget',
        'account_cancel',
        # 'account_followup', -- deprecated
        #'account_payment', -- deprecated
        'analytic',
        #'analytic_user_function', -- deprecated
        'auth_signup',
        'auth_crypt',
        'base',
        'base_action_rule',
        'base_iban',
        'base_import',
        #'base_report_designer', -- deprecated
        'base_setup',
        'board',
        'bus',
        'calendar',
        'claim_from_delivery',
        'crm_claim',
        'crm_helpdesk',
        #'crm_profiling', --- deprecated
        'decimal_precision',
        'delivery',
        'document',
        #'edi', -- deprecated
        #'email_template', -- deprecated
        'fetchmail',
        'hr_attendance',
        'hr_contract',
        'hr_payroll_account',
        #'hr_timesheet_invoice', -- deprecated
        'lunch',
        'marketing',
        'marketing_campaign',
        #'marketing_crm', -- deprecated
        'mrp_byproduct',
        'mrp_operations',
        'mrp_repair',
        'payment',
        'payment_transfer',
        'procurement',
        'procurement_jit',
        #'procurement_jit_stock', -- deprecated
        'product',
        'project_issue_sheet',
        'project_timesheet',
        #'purchase_double_validation', -- deprecated
        'purchase_requisition',
        'report',
        'resource',
        'sale_crm',
        #'sale_journal', -- deprecated
        'sale_margin',
        'sale_mrp',
        'sale_order_dates',
        'sales_team',
        'sale_stock',
        #'share', -- deprecated
        'subscription',
        'warning',
        #'account_check_writing', --deprecated
        'account_check_printing',
        'web_calendar',
        #'account_anglo_saxon', -- deprecated
        'web',
        'web_diagram',
        #'web_gantt', -- deprecated
        #'web_graph', -- deprecated
        'web_kanban',
        'web_kanban_gauge',
        #'web_kanban_sparkline', -- deprecated
        # 'web_tests', -- deprecated
        'web_view_editor',
        'report_webkit',
        #'account_analytic_analysis', -- deprecated
        #
        # OCA/account-financial-reporting
        #'account_financial_report_webkit', -- deprecated
        'account_financial_report_qweb',
        #
        # OCA/account-financial-tools
        'account_move_line_purchase_info', # PR https://github.com/OCA/account-financial-tools/pull/444
        # OCA/product-attribute
        # ---------------------
        'product_manufacturer',
        #
        # OCA/knowledge
        # -------------
        'knowledge',
        'document_page',
        #
        # OCA/server-tools
        # ----------------
        'base_technical_features',
        'database_cleanup',
        'auditlog',
        'base_search_fuzzy',
        #
        # OCA/stock-logistics-warehouse
        # ---------------------
        'stock_putaway_product',
        'stock_orderpoint_manual_procurement',
        'stock_orderpoint_uom',
        'stock_inventory_revaluation', # PR https://github.com/OCA/stock-logistics-warehouse/pull/213
        'stock_valuation_account_manual_adjustment',
        'account_move_line_product',
        'stock_quant_reserved_qty_uom', # PR https://github.com/OCA/stock-logistics-warehouse/pull/216
        'account_move_line_stock_info',
        'stock_quant_merge',
        #
        # OCA/account-invoicing
        # ---------------------
        'account_invoice_merge',
        #
        # OCA/purchase-workflow
        # ---------------------
        'product_by_supplier',
        'purchase_location_by_line', # PR https://github.com/OCA/purchase-workflow/pull/313
        'purchase_delivery_split_date',
        'purchase_request_procurement',
        'purchase_request',
        'purchase_request_to_requisition',
        'purchase_request_to_rfq',
        'purchase_delivery_split_date',
        #
        # OCA/hr-timesheet
        # ----------------
        'hr_timesheet_sheet_week_start_day',
        #
        # OCA/web
        # -------
        'web_widget_x2many_2d_matrix',
        'web_sheet_full_width',
        'web_export_view',
        'web_tree_dynamic_colored_field',
        #
        # OCA/sale-workflow
        # -----------------
        # 'sale_stock_picking_back2draft', -- not yet ported to v9
        'stock_picking_back2draft', # PR https://github.com/OCA/stock-logistics-workflow/pull/276
        'sale_procurement_group_by_line', # PR https://github.com/OCA/sale-workflow/pull/350
        'sale_sourced_by_line', # PR https://github.com/OCA/sale-workflow/pull/350
        #
        # OCA/bank-statement-reconcile
        # 'account_easy_reconcile', -- migrated to account_mass_reconcile
        # 'account_advanced_reconcile', -- migrated to account_mass_reconcile
        # 'account_mass_reconcile', -- pending to install
        # 'account_advanced_reconcile_transaction_by_purchase_line', -- pending to migrate
        #
        # OCA/connector-telephony
        # 'asterisk_click2dial', -- not used
        # 'base_phone', -- not used
        # 'crm_phone', -- not used
        #'asterisk_click2dial_crm', -- deprecated
        #
        # OCA/crm
        'crm_deduplicate_acl',
        #
        # OCA/social
        #'mail_debrand', -- Pending to migrate
        # 'mail_message_name_search', --deprecated
        #
        'base_search_mail_content',
        # OCA/account-payment
        # -------------------
        'account_due_list', # PR: https://github.com/OCA/account-payment/pull/122
        'account_due_list_aging_comments', # PR: https://github.com/OCA/account-payment/pull/124
        'account_due_list_days_overdue', # PR: https://github.com/OCA/account-payment/pull/123
        #
        # Vauxoo
        #'product_do_merge', -- deprecated
        #
        # WilldooIT/Pentaho-reports-for-OpenERP
        # 'pentaho_reports' -- deprecated
        #
        # Eficent/ddmrp
        # -------------
        'ddmrp',
        'stock_available_unreserved',
        'stock_demand_estimate',
        'stock_warehouse_orderpoint_stock_info',
        #'account_bank_statement_extensions', -- deprecated
        #'l10n_be_coda', -- deprecated
        # 'l10n_be_invoice_bba', -- deprecated
        # 'account_financial_report_webkit_xls', --deprecated
        #'report_xls', -- deprecated
        # OCA/reporting-engine
        #
        'bi_view_editor', # PR: https://github.com/OCA/reporting-engine/pull/59
        #
        # ao-odoo
        # -------
        'smile_decimal_precision',
        # 'ursa_web_style', -- deprecated
        # 'partner_aging', -- deprecated
        'ursa_product_reference',
        'usa_localization',
        'ursa_product_gtin',
        # 'account_fstr', -- deprecated
        'ursa_crmlead',
        'ursa_helpdesk',
        'ursa_product_customizations',
        'ursa_ref_partner',
        # 'stock_picking_preview_putaway_location', -- deprecated
        # 'ursa_sale_customizations', -- deprecated
        # 'ursa_shipwire', -- deprecated
        'ao_account',
        # 'ao_account_check_writing', -- deprecated
        'ao_account_due_list',
        # 'ao_account_voucher', -- deprecated
        # 'ao_crm_helpdesk', -- deprecated
        # 'ao_hr', -- deprecated
        # 'ao_hr_payroll', -- deprecated
        'ao_hr_timesheet_sheet',
        'ao_login_rename',
        # 'ao_mail_debrand', --pending to migrate
        'ao_mrp',
        'ao_product',
        'ao_project',
        'ao_purchase',
        'ao_purchase_dept',
        'ao_sale',
        # 'ao_stock', -- deprecated
        'ao_stock_account',
        'stock_picking_menu',
        'stock_picking_sale_note',
        'account_anglo_saxon_no_cogs_deferral',
        'mrp_production_calculate_cost_finished_product',
        'mrp_production_update_product_price',
        'product_bom_standard_cost',
        'stock_account_change_product_valuation',
        'crm_helpdesk_button_open',
        'mrp_production_service',
        # 'product_uom_change_fix', --deprecated
        # 'stock_picking_report_reserved_quant', -- deprecated
        # 'ursa_purchase_customizations', --deprecated
    ],
    'installable': True,
}
