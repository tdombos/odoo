from odoo import models, fields

class WebsitePage(models.Model):
    _inherit = 'website.page'

    background_image = fields.Image("Background image", help="Background image for page.")
