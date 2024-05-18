# -*- coding: utf-8 -*-
from werkzeug import urls

from odoo import api, fields, Command, models, _
from odoo.tools.translate import html_translate
from odoo.exceptions import UserError

class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    payment_online = fields.Boolean('Online', help="Expense paid online by company bankcard", tracking=True)
    partner_name = fields.Char('Partner name',  tracking=True)
    partner_email = fields.Char('Partner email',  tracking=True)
    partner_tax = fields.Char('Partner tax',  tracking=True)
    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        domain=[("res_model", "=", "hr.expense")],
        string="Attachments",
    )