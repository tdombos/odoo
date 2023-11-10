# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskMgmtPartnerSecurity(http.Controller):
#     @http.route('/helpdesk_mgmt_partner_security/helpdesk_mgmt_partner_security', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_mgmt_partner_security/helpdesk_mgmt_partner_security/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_mgmt_partner_security.listing', {
#             'root': '/helpdesk_mgmt_partner_security/helpdesk_mgmt_partner_security',
#             'objects': http.request.env['helpdesk_mgmt_partner_security.helpdesk_mgmt_partner_security'].search([]),
#         })

#     @http.route('/helpdesk_mgmt_partner_security/helpdesk_mgmt_partner_security/objects/<model("helpdesk_mgmt_partner_security.helpdesk_mgmt_partner_security"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_mgmt_partner_security.object', {
#             'object': obj
#         })
