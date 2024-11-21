from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import unslug, slug

class EmployeeSnippetController(http.Controller):

       @http.route('/api/partnersByCategory', type='json', auth='public', website=True)
       def employees_by_category(self, category_id=None):
           domain = [('web_category', '=', category_id)]
           partners = request.env['res.partner'].search(domain, order="name asc")
           ##listTpl = request.env['ir.ui.view']._render_template(
           ##    'website_partner_highlight.list',
           ##    {'partners': partners}
           ##)
           ##return {'html': listTpl.encode('utf-8')}
           return [{"id": partner["id"], "name": partner["name"], "website": partner["website"]} for partner in partners]
