# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class product_product(models.Model):
    _inherit = 'product.product'
    
    book_category_id = fields.Many2one('product.category', string="Book Category", required=0)
    language = fields.Many2many('res.lang', string="Language")
    
class library_card(models.Model):
    _inherit = 'dev.library.card'
    
    @api.onchange('membership_id')
    def onchange_membership(self):
        if self.membership_id:
            self.member_id = self.membership_id.partner.id 
            self.mobile = self.member_id.mobile
            self.email = self.member_id.email
            self.validity_date = self.membership_id.date_to
    
    def get_qr_data(self):
        data = ''
        if self.name:
            data = data + str(self.name)
        return data