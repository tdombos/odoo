odoo.define('hr_profile_page.dynamic_employee_snippet', ["@web/legacy/js/public/public_widget","@web/core/network/rpc_service"], function (require) {

    const publicWidget = require("@web/legacy/js/public/public_widget")[Symbol.for("default")];
    const rpc = require("@web/core/network/rpc_service");

    publicWidget.registry.DynamicEmployeeSnippet = publicWidget.Widget.extend({
        selector: '.employee_card_snippet',
        events: {
            'click [data-category-id]': '_onCategoryChange',
        },
        disabledInEditableMode: false,

        start: function () {
            this._fetchEmployees(this.$el[0].dataset.categoryId);
            return this._super.apply(this, arguments);
        },

        _onCategoryChange: function (ev) {
            this._fetchEmployees(this.$el[0].dataset.categoryId);
        },

        _fetchEmployees: function (categoryId) {
            var self = this;
            if (categoryId) {
                rpc.jsonrpc('/api/employeesByCategory', {category_id: categoryId}).then(function (data) {
                    self._renderEmployees(data.html);
                });
            }
        },

        _renderEmployees: function (html) {
            var $container = this.$('.employee-cards');
            $container.html(html);
        },
    });
});