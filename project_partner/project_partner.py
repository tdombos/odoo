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


from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.addons.project import project

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.addons.project import project

class project_partner_partnerline(models.Model):
    _name = 'project_partner.partnerline'
    _description = 'Partner'
    
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    project_id = fields.Many2one('project.project', string='Project', required=True, ondelete='cascade')
    role_id = fields.Many2one('project_partner.role', string='Role')
    state = fields.Selection([('open', 'Current'),('close', 'Archived')], string='State', size=16)
    
    _defaults = {
        'state': 'open',
    }
    _rec_name = 'partner_id'
    
    @api.one
    def do_open(self):
        self.state = 'open'
        return True
    def do_close(self):
        self.state = 'close'
        return True
        
class project_partner_role(models.Model):
    _name = 'project_partner.role'
    _description = 'Roles'
    
    name = fields.Char('Name', size=64, required=True)
    description = fields.Text('Description', help='Detailed description for the role')

    _sql_constraints = [
        ('name', 'unique(name)', 'Tag name has to be unique')
    ]
    _order = 'name asc'

class project_project(models.Model):
    _inherit = ['project.project']
    partnerline_ids = fields.One2many('project_partner.partnerline', 'project_id', "Partners")
    
    @api.depends('partnerline_ids')
    def _partner_count(self):
        for record in self:
            record.count = len(record.partnerline_ids)
    partner_count = fields.Integer(compute='_partner_count', string="Partners",)

