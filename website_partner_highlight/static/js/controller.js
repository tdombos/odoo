odoo.define('website_partner_highlight.dynamic_list_snippet', ["@web/legacy/js/public/public_widget", "@web/core/network/rpc_service"], function (require) {

    const publicWidget = require("@web/legacy/js/public/public_widget")[Symbol.for("default")];
    const rpc = require("@web/core/network/rpc_service");

    publicWidget.registry.DynamicPartnerListSnippet = publicWidget.Widget.extend({
        selector: '.partners_snippet',
        events: {
            'click [data-category-id]': '_onCategoryChange',
        },
        disabledInEditableMode: false,

        start: function () {
            this._fetchPartners(this.$el[0].dataset.categoryId);
            return this._super.apply(this, arguments);
        },

        _onCategoryChange: function (ev) {
            this._fetchPartners(this.$el[0].dataset.categoryId);
        },

        _fetchPartners: function (categoryId) {
            const self = this;
            if (categoryId) {
                rpc.jsonrpc('/api/partnersByCategory', {category_id: categoryId}).then(function (data) {
                    self._renderPartners(data);
                });
            }
        },

        _renderPartners: function (partners) {
            const $container = this.$('.partner-list');
            const items = Array.isArray(partners) ? partners.map(function (partner) {
                if (partner.website) {
                    return `<a class="h-100 flex-column" href="${partner.website}" target="_blank">
                <img src="/public/image/partner/${partner.id}" alt=${partner.name}/></a>`;
                } else {
                    return `<span class="h-100 flex-column">
                <img src="/public/image/partner/${partner.id}" alt=${partner.name}/></span>`;
                }
            }) : [];
            $container.html(items.join('\n'));
        },
    });
});