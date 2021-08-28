# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from odoo import exceptions

class project_partner_partnerline(models.Model):
    _name = 'project_partner.partnerline'
    _description = 'Partner'
    
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    task_id = fields.Many2one('project.task', string='Task', ondelete='cascade')
    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade')
    role_id = fields.Many2one('project_partner.role', string='Role')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the partner without removing it.", default=True)
    
    _rec_name = 'partner_id'

        
class project_partner_role(models.Model):
    _name = 'project_partner.role'
    _description = 'Roles'
    
    name = fields.Char('Name', size=64, required=True,translate=True)
    description = fields.Text('Description', help='Detailed description for the role')

    _sql_constraints = [
        ('name', 'unique(name)', 'Tag name has to be unique')
    ]
    _order = 'name asc'

class project_task(models.Model):
    _inherit = ['project.task']
    
    @api.depends('partnerline_ids')
    def _partner_count(self):
        for record in self:
            record.partner_count = len(record.partnerline_ids)
            
    partnerline_ids = fields.One2many('project_partner.partnerline', 'task_id', "Partners")
    partner_count = fields.Integer(compute='_partner_count', string="Partners",)

class project_project(models.Model):
    _inherit = ['project.project']
    
    @api.depends('partnerline_ids')
    def _partner_count(self):
        for record in self:
            record.partner_count = len(record.partnerline_ids)
            
    partnerline_ids = fields.One2many('project_partner.partnerline', 'project_id', "Partners")
    partner_count = fields.Integer(compute='_partner_count', string="Partners",)
