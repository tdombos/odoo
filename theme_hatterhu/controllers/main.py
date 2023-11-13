# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug.urls

from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug, slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.tools.translate import _
from odoo.http import request


class WebsiteEmployee(http.Controller):
    _references_per_page = 200
    @http.route(['/egyesuletunk/munkatarsaink'], type='http', auth="public", website=True)
    def employee_list(self, **post):
        Employee = request.env['hr.employee']

        domain = []
        employees = Employee.sudo().search(domain, offset=0, limit=self._references_per_page)
        employee_count = Employee.sudo().search_count(domain)


        return request.render("theme_hatterhu.employee_list", {'employees': employees, 'employee_count': {'count': employee_count}})

    # Do not use semantic controller due to SUPERUSER_ID
    @http.route(['/egyesuletunk/munkatarsaink/<employee_id>'], type='http', auth="public", website=True)
    def employee_detail(self, employee_id, **post):
        employee_id = unslug(employee_id)
        if employee_id:
            employee = request.env['hr.employee'].sudo().browse(employee_id)
            if employee.exists(): # and employee.website_published:
                values = {}
                values['main_object'] = values['employee'] = employee
                return request.render("theme_hatterhu.employee_detail", values)
        return self.employee_list(**post)
