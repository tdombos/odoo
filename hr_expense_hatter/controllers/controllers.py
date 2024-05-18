# -*- coding: utf-8 -*-
# from odoo import http


# class HrHatter(http.Controller):
#     @http.route('/hr_hatter/hr_hatter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_hatter/hr_hatter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_hatter.listing', {
#             'root': '/hr_hatter/hr_hatter',
#             'objects': http.request.env['hr_hatter.hr_hatter'].search([]),
#         })

#     @http.route('/hr_hatter/hr_hatter/objects/<model("hr_hatter.hr_hatter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_hatter.object', {
#             'object': obj
#         })
