# -*- coding: utf-8 -*-
# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'AO Profile',
    'version': '10.0.1.0.0',
    'author': 'Aleph Objects Inc.',
    'summary': 'Contains the modules used by AO',
    'website': 'http://www.eficent.com',
    'category': 'Customizations',
    'depends': [
        # Odoo standard
        # -------------
        # 'account_analytic_analysis', -- deprecated
        # 'account_analytic_default', -- deprecated
        # 'account_analytic_plans', -- deprecated
        # 'account_anglo_saxon', -- deprecated
        # 'account_check_writing', --deprecated
        # 'account_followup', -- deprecated
        # 'account_payment', -- deprecated
        # 'analytic_contract_hr_expense', -- deprecated
        # 'analytic_user_function', -- deprecated
        # 'base_report_designer', -- deprecated
        # 'claim_from_delivery', -- deprecated in v10
        # 'crm_profiling', --- deprecated
        # 'edi', -- deprecated
        # 'email_template', -- deprecated
        # 'hr_timesheet_invoice', -- deprecated
        # 'marketing', --deprecated in v10
        # 'marketing_crm', -- deprecated
        # 'mrp_operations', --deprecated in v10
        # 'procurement_jit',  -- not with ddmrp (beware: it's auto-installed)
        # 'procurement_jit_stock', -- deprecated
        # 'project_timesheet',  # Merged in hr_timesheet in v10
        # 'purchase_double_validation', -- deprecated
        # 'report_webkit', -- deprecated in v10 (openupgrade pending)
        # 'sale_journal', -- deprecated
        # 'share', -- deprecated
        # 'warning', --deprecated in v10
        # 'web_gantt', -- deprecated
        # 'web_graph', -- deprecated
        # 'web_kanban_sparkline', -- deprecated
        # 'web_tests', -- deprecated
        # 'web_view_editor', --deprecated in v10
        'account',
        'account_accountant',
        'account_asset',
        'account_budget',
        'account_cancel',
        'account_check_printing',
        'account_voucher',
        'analytic',
        'auth_crypt',
        'auth_signup',
        'base',
        'base_action_rule',
        'base_iban',
        'base_import',
        'base_setup',
        'board',
        'bus',
        'calendar',
        'crm',
        'decimal_precision',
        'delivery',
        'document',
        'fetchmail',
        'hr',
        'hr_attendance',
        'hr_contract',
        'hr_expense',
        'hr_holidays',
        'hr_payroll',
        'hr_payroll_account',
        'hr_timesheet',
        'hr_timesheet_sheet',
        'lunch',
        'mail',
        'marketing_campaign',
        'mrp',
        'mrp_byproduct',
        'mrp_repair',
        'note',
        'payment',
        'payment_transfer',
        'point_of_sale',
        'procurement',
        'product',
        'project',
        'project_issue',  # gives error
        'project_issue_sheet',  # gives error
        'purchase',
        'purchase_requisition',
        'report',
        'resource',
        'sale',
        'sale_crm',
        'sale_margin',
        'sale_mrp',
        'sale_order_dates',
        'sale_stock',
        'sales_team',
        'stock',
        'stock_account',
        'subscription',
        'web',
        'web_calendar',
        'web_diagram',
        'web_kanban',
        'web_kanban_gauge',
        #
        # OCA/account-financial-reporting
        # -------------------------------
        #'account_financial_report_webkit', -- deprecated
        'account_financial_report_qweb',
        'customer_activity_statement',
        'customer_outstanding_statement',
        'account_tax_balance',
        #
        # OCA/mis-builder
        # ---------------
        'mis_builder',
        #
        # OCA/account-financial-tools
        # ---------------------------
        'account_move_line_purchase_info',
        #
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
        'auditlog',
        'base_search_fuzzy',
        'base_technical_features',
        'database_cleanup',
        'disable_odoo_online',
        #
        # OCA/stock-logistics-warehouse
        # ---------------------
        'account_move_line_product',
        'account_move_line_stock_info',
        'stock_account_quant_merge',
        'stock_available_unreserved',
        'stock_cycle_count',
        'stock_demand_estimate',
        'stock_inventory_exclude_sublocation',
        'stock_inventory_revaluation',
        'stock_inventory_verification_request',
        'stock_orderpoint_manual_procurement',  # under rework
        'stock_orderpoint_uom',
        'stock_putaway_product',
        'stock_quant_merge',
        'stock_quant_reserved_qty_uom',
        'stock_valuation_account_manual_adjustment',  # to be migrated
        'stock_warehouse_orderpoint_stock_info',
        'stock_warehouse_orderpoint_stock_info_unreserved',
        'stock_inventory_chatter',
        'stock_removal_location_by_priority',
        'procurement_auto_create_group',
        'stock_account_change_product_valuation',
        # 'stock_picking_back2draft', Deprecated - See
        # https://github.com/OCA/stock-logistics-workflow/pull/276
        #
        # OCA/stock-logistics-workflow
        # ----------------------------
        'stock_disable_force_availability_button',
        'stock_no_negative',
        'stock_picking_operation_quick_change',
        #
        # OCA/account-invoicing
        # ---------------------
        # 'account_invoice_refund_option', -- Deprecaded, https://github.com/OCA/account-invoicing/pull/229
        'account_invoice_merge',
        'account_invoice_view_payment',
        'purchase_stock_picking_return_invoicing',
        'sale_stock_picking_return_invoicing',
        'purchase_stock_picking_return_invoicing_open_qty',  # TODO: not migrated
        'account_invoice_fixed_discount',
        #
        # OCA/purchase-workflow
        # ---------------------
        'product_by_supplier',
        'purchase_delivery_split_date',
        'purchase_delivery_split_date',
        'purchase_location_by_line',
        'purchase_open_qty',
        'purchase_order_approved',
        'purchase_request',
        'purchase_request_department',
        'purchase_request_procurement',
        'purchase_request_to_procurement',
        'purchase_request_to_requisition',  # Maybe not needed
        'purchase_request_to_rfq',
        'purchase_request_to_rfq_order_approved',
        'subcontracted_service',
        #
        # OCA/hr
        # ------
        'hr_holidays_notify_employee_manager',  # v9: hr_holiday_notify_employee_manager
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
        'web_tree_many2one_clickable',
        #
        # OCA/sale-workflow
        # -----------------
        # 'sale_sourced_by_line',  -- not needed, feature is out-of-the-box.
        # 'sale_stock_picking_back2draft', -- not yet ported to v9, see stock_picking_back2draft
        'sale_force_invoiced',
        'sale_procurement_group_by_line',
        'sale_product_set',
        'sale_validity',
        'sale_fixed_discount',
        #
        # OCA/account-reconcile
        # ---------------------
        'account_mass_reconcile',
        'account_mass_reconcile_by_purchase_line',
        #
        # OCA/crm
        # -------
        'crm_claim',
        'crm_helpdesk',
        'crm_deduplicate_acl',
        'crm_sale_marketing',
        #
        # OCA/partner-contact
        # -------------------
        'partner_contact_job_position',
        'partner_sector',
        #
        # OCA/social
        # ----------
        # 'mail_debrand', -- integrated in ao_mail
        # 'mail_message_name_search', --deprecated
        'base_search_mail_content',
        'mail_tracking',
        #
        # OCA/account-payment
        # -------------------
        'account_due_list',
        'account_due_list_aging_comments',
        'account_due_list_days_overdue',
        'account_check_printing_report_base',
        'account_check_printing_report_dlt103',
        'account_partner_reconcile',
        'account_payment_show_invoice',
        #
        # OCA/manufacture
        # -------------------------
        # 'mrp_production_unreserve', -- not needed in v10
        'mrp_bom_component_menu',
        'mrp_mto_with_stock',
        'mrp_production_putaway_strategy',
        'mrp_production_request',  #TODO: To be migrated to v10
        # 'mrp_disable_force_availability_button', -- deprecated, trust stock_no_negative
        #
        # OCA/manufacture-reporting
        # -------------------------
        'mrp_bom_structure_report_level_1',
        'mrp_bom_structure_xlsx',
        'mrp_bom_structure_xlsx_level_1',
        #
        # OCA/project-reporting
        # ---------------------
        'project_task_report',
        #
        # Eficent/ddmrp
        # -------------
        'ddmrp', # to be migrated to v10
        'ddmrp_exclude_moves_adu_calc',
        'ddmrp_history',
        'ddmrp_mrp_production_request'
        'ddmrp_product_replace',
        'procurement_service',  # also OCA/manufacture, really needed?
        #
        # 'account_bank_statement_extensions', -- deprecated
        # 'l10n_be_coda', -- deprecated
        # 'l10n_be_invoice_bba', -- deprecated
        #
        # OCA/reporting-engine
        # --------------------
        'bi_sql_editor',
        'bi_view_editor',
        'report_wkhtmltopdf_param',
        #
        # ao-odoo
        # -------
        # 'account_fstr', -- deprecated
        # 'ao_account_check_writing', -- deprecated
        # 'ao_account_voucher', -- deprecated
        # 'ao_crm_helpdesk', -- deprecated
        # 'ao_hr', -- deprecated
        # 'ao_hr_holidays',  -- standard behavior since v10
        # 'ao_hr_payroll', -- deprecated
        # 'ao_mail_debrand', --pending to migrate
        # 'ao_product', -- standard behavior since v10
        # 'ao_project', -- deprecated in v10
        # 'ao_stock_account', --deprecated
        # 'mail_auto_follower_notify', -- seems to work out of the box. needed?
        # 'partner_aging', -- deprecated
        # 'product_uom_change_fix', --deprecated
        # 'smile_decimal_precision', -- deprecated, not needed.
        # 'stock_picking_preview_putaway_location', -- deprecated
        # 'stock_picking_report_reserved_quant', -- deprecated
        # 'ursa_purchase_customizations', --deprecated
        # 'ursa_sale_customizations', -- deprecated
        # 'ursa_shipwire', -- deprecated
        # 'ursa_web_style', -- deprecated
        'account_anglo_saxon_no_cogs_deferral',
        'ao_account',
        'ao_account_due_list',
        'ao_base',
        'ao_crm',
        'ao_crm_helpdesk_parse_email_lulzbot_support',
        'ao_crm_lead_parse_email',
        'ao_hr_timesheet_sheet',
        'ao_login_rename',
        'ao_mail',
        'ao_mrp',
        'ao_purchase',
        'ao_purchase_dept',
        'ao_sale',
        'ao_stock',
        'ao_stock_picking_operation_quick_change',
        'ao_stock_scrap',
        'ao_utm',
        'ao_web',
        'crm_helpdesk_add_suggested_recipient',  # needed?
        'crm_helpdesk_button_open',
        'crm_helpdesk_warning',
        'mrp_production_calculate_cost_finished_product',
        'mrp_production_service',  # issue: procurement are not being set to done.
        'mrp_production_update_product_price',
        'product_bom_standard_cost',
        'project_task_work',
        'stock_picking_menu',
        'stock_picking_sale_note',
        'ursa_crmlead',
        'ursa_helpdesk',
        'ursa_product_customizations',
        'ursa_product_gtin',
        'ursa_product_reference',
        'ursa_ref_partner',
        'usa_localization',
    ],
    'installable': True,
}
