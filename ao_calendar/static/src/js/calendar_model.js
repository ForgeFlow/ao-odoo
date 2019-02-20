odoo.define('web.CalendarModel2', function (require) {
"use strict";
    var CalendarModel = require('web.CalendarModel');
    var Context = require('web.Context');
    var core = require('web.core');
    var fieldUtils = require('web.field_utils');
    var session = require('web.session');
    var time = require('web.time');


    return CalendarModel.include({
        _getFullCalendarOptions: function () {
            var self = this;
            var options = this._super();
            self._rpc({
                model: "res.users",
                method: 'search_read',
                fields: ['calendar_allow_ui_edition'],
                domain: [['id', '=', self.data.context.uid]]
            })
            .then(function (result) {
                var editable = result[0]['calendar_allow_ui_edition']
                options.editable = editable
            });
            return options;
        },
    });
});