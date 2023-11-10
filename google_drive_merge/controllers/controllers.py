# -*- coding: utf-8 -*-
# from odoo import http


# class PartnerResidingAddress(http.Controller):
#     @http.route('/partner_residing_address/partner_residing_address/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_residing_address/partner_residing_address/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_residing_address.listing', {
#             'root': '/partner_residing_address/partner_residing_address',
#             'objects': http.request.env['partner_residing_address.partner_residing_address'].search([]),
#         })

#     @http.route('/partner_residing_address/partner_residing_address/objects/<model("partner_residing_address.partner_residing_address"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_residing_address.object', {
#             'object': obj
#         })
