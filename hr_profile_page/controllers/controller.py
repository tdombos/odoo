from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import unslug, slug

class EmployeeSnippetController(http.Controller):

       @http.route('/api/employeesByCategory', type='json', auth='public', website=True)
       def employees_by_category(self, category_id=None):
           domain = [('web_category', '=', category_id)]
           employees = request.env['hr.employee'].sudo().search(domain, order="name asc")
           employee_cards = request.env['ir.ui.view']._render_template(
               'hr_profile_page.employee_card_list',
               {'employees': employees}
           )
           return {'html': employee_cards.encode('utf-8')}

       @http.route(['/egyesuletunk/munkatarsaink/<employee_id>'], type='http', auth="public", website=True)
       def employee_detail(self, employee_id, **post):
           employee_id = unslug(employee_id)[1]
           if employee_id:
               employee = request.env['hr.employee'].sudo().browse(employee_id)
               if employee.exists(): # and employee.website_published:
                   values = {}
                   values['main_object'] = values['employee'] = employee
                   return request.render("hr_profile_page.employee_detail", values)
