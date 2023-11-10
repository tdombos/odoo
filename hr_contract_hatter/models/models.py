# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContractType(models.Model):
    _name = 'hr.contract.type'
    _description = 'Contract Type'
    _order = 'sequence, id'

    name = fields.Char(string='Contract Type', required=True, help="Name")
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Contract.", default=10)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the folder without removing it.", default=True)
    
class Contract(models.Model):
    _inherit = ['hr.contract']

    parent_id = fields.Many2one('hr.contract', 'Main contract')
    state = fields.Selection(selection_add=[('sign', 'Signing')])
    type_id = fields.Many2one('hr.contract.type', string="Contract type", required=True, help="Type of the contract")
    project_id = fields.Many2one('project.project', string='Project', help="Project the contract is related to")


