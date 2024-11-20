odoo.define('website_partner_highlight.dynamic_list_snippet', ["@web/legacy/js/public/public_widget","@web/core/network/rpc_service"], function (require) {

    const publicWidget = require("@web/legacy/js/public/public_widget")[Symbol.for("default")];
    const rpc = require("@web/core/network/rpc_service");

    publicWidget.registry.DynamicPartnerListSnippet = publicWidget.Widget.extend({
        selector: '.partners_snippet',
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
            const self = this;
            if (categoryId) {
                rpc.jsonrpc('/api/partnersByCategory', {category_id: categoryId}).then(function (data) {
                    self._renderPartners(data.html);
                });
            }
        },

        _renderPartners: function (html) {
            const $container = this.$('.partner-list');
            $container.html(html);
        },
    });
});