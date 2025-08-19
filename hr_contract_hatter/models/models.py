# -*- coding: utf-8 -*-

from odoo import models, fields, api
    
class Contract(models.Model):
    _inherit = ['hr.contract']

    parent_id = fields.Many2one('hr.contract', 'Main contract')
    state = fields.Selection(selection_add=[('sign', 'Signing')])
    project_id = fields.Many2one('project.project', string='Project', help="Project the contract is related to")


