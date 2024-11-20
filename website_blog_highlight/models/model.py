from odoo import fields, models

class BlogPostHighlightModel(models.Model):
    _inherit = "blog.post"

    is_highlighted = fields.Boolean("Highlighted", default=False)