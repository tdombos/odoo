# -*- coding: utf-8 -*-
# from odoo import http


# class HrContractHatter(http.Controller):
#     @http.route('/hr_contract_hatter/hr_contract_hatter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_contract_hatter/hr_contract_hatter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_contract_hatter.listing', {
#             'root': '/hr_contract_hatter/hr_contract_hatter',
#             'objects': http.request.env['hr_contract_hatter.hr_contract_hatter'].search([]),
#         })

#     @http.route('/hr_contract_hatter/hr_contract_hatter/objects/<model("hr_contract_hatter.hr_contract_hatter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_contract_hatter.object', {
#             'object': obj
#         })
