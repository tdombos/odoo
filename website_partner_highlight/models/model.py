from odoo import fields, models

class ResPartnerHighlightModel(models.Model):
    _inherit = "res.partner"

    highlight_category =  web_category = fields.Selection(
        selection=[
            ('none', 'None'),
            ('partner', 'Partner'),
            ('supporter', 'Supporter')
        ],
        string='Web Category',
        default='none',
    ) 