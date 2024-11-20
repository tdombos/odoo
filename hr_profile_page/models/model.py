from odoo import fields, models

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    web_category = fields.Selection(
        selection=[
            ('none', 'None'),
            ('official', 'Official'),
            ('colleague', 'Colleague'),
            ('former_colleague', 'Former Colleague')
        ],
        string='Web Category',
        default='none',
    )
    introduction = fields.Html(string="Introduction")



