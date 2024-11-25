from odoo import http
from odoo.http import request, Stream
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

    @http.route(['/egyesuletunk/munkatarsaink/<employee_slug>'], type='http', auth="public", website=True)
    def employee_detail(self, employee_slug, **post):
       employee_id = unslug(employee_slug)[1]
       if employee_id:
           employee = request.env['hr.employee'].sudo().browse(employee_id)
           if employee.exists(): # and employee.website_published:
               values = {}
               values['main_object'] = values['employee'] = employee
               return request.render("hr_profile_page.employee_detail", values)


    @http.route('/public/image/employee/<int:employee_id>', type='http', auth='public', website=True)
    def public_employee_image(self, employee_id):
        employee = request.env['hr.employee'].sudo().browse(employee_id)
        if not employee.exists():
            return request.not_found()

        image = request.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'hr.employee'),
            ('res_id', '=', employee_id),
            ('res_field', '=', 'image_512')
            ], limit=1
        )

        if not image.exists():
            return request.not_found()

        return Stream.from_binary_field(employee,'image_512').get_response(mimetype=image.mimetype)
