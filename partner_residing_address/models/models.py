# -*- coding: utf-8 -*-

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('residing', 'Residing address')])