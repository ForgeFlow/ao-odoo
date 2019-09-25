odoo.define('mrp_bom_standard_cost.mrp_bom_standard_cost_report_widget', function (require) {
    'use strict';

    var Widget = require('web.Widget');


    var mrpBomStandardCostReportWidget = Widget.extend({
        events: {
            'click .o_bom_standard_cost_product': 'boundLink',
        },
        init: function() {
            console.log("Init")
            this._super.apply(this, arguments);
        },
        start: function() {
            console.log("Start")
            return this._super.apply(this, arguments);
        },
        boundLink: function(e) {
            console.log("BoundLink")
            var res_model = $(e.target).data('res-model');
            var res_id = $(e.target).data('active-id');
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: res_model,
                res_id: res_id,
                views: [[false, 'form']],
                target: 'current'
            });
        },
    });

    return mrpBomStandardCostReportWidget;

});
