# -*- coding: utf-8 -*-
# from odoo import http


# class HrPartnerSecurity(http.Controller):
#     @http.route('/hr_partner_security/hr_partner_security', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_partner_security/hr_partner_security/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_partner_security.listing', {
#             'root': '/hr_partner_security/hr_partner_security',
#             'objects': http.request.env['hr_partner_security.hr_partner_security'].search([]),
#         })

#     @http.route('/hr_partner_security/hr_partner_security/objects/<model("hr_partner_security.hr_partner_security"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_partner_security.object', {
#             'object': obj
#         })
