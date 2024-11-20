from odoo import models, fields

class WebsitePage(models.Model):
    _inherit = 'website.page'

    background_image = fields.Image("Background Image", help="Background image for page.")


    def getBgStyle(self):
        self.ensure_one()  # Ensure that we are working with a single record
        style = f"background-image: url('/web/image/website.page/{self.id}/background_image')"
        _logger.debug("Generated style: %s", style)
        return style