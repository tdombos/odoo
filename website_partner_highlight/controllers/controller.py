from odoo import http
from odoo.http import request, Stream
from odoo.addons.http_routing.models.ir_http import unslug, slug

class EmployeeSnippetController(http.Controller):

    @http.route('/api/partnersByCategory', type='json', auth='public', website=True)
    def employees_by_category(self, category_id=None):
       domain = [('web_category', '=', category_id)]
       partners = request.env['res.partner'].sudo().search(domain, order="name asc")
       ##listTpl = request.env['ir.ui.view']._render_template(
       ##    'website_partner_highlight.list',
       ##    {'partners': partners}
       ##)
       ##return {'html': listTpl.encode('utf-8')}
       return [{"id": partner["id"], "name": partner["name"], "website": partner["website"]} for partner in partners]


    @http.route('/public/image/partner/<int:partner_id>', type='http', auth='public', website=True)
    def public_partner_image(self, partner_id):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return request.not_found()
        image = request.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'res.partner'),
            ('res_id', '=', partner_id),
            ('res_field', '=', 'image_512')
            ], limit=1
        )

        if not image.exists():
            return request.not_found()

        return Stream.from_binary_field(partner,'image_512').get_response(mimetype=image.mimetype)