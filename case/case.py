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

from odoo import models, fields, api, SUPERUSER_ID
from odoo import exceptions
            
class case_case(models.Model):
    _name = 'case.case'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Case'
    _inherits = {
        'project.task': 'task_id',
    }
    
    @api.depends('activity_ids')
    def _activity_count(self):
        for record in self:
            record.activity_count = len(record.activity_ids)
            
    @api.multi
    def _compute_attached_docs_count(self):
        Doc = self.env['case.document']
        for case in self:
            case.doc_count = Doc.search_count([
               ('case_id', '=', case.id)
            ])

    
    title = fields.Char('Title', select=True)
    task_id = fields.Many2one('project.task', required=True, string='Related Task', ondelete='restrict', help='Task-related data of the case', auto_join=True)
    date_start = fields.Date(string='Case arrived',
        default='',
        index=True, copy=False)
    date_end = fields.Date(string='Case closed',
        default='',
        index=True, copy=False)
    externalref = fields.Text('External References', track_visibility='onchange')
    description_anon = fields.Html('Anonymized Summary')
    servicelevel_ids = fields.Many2many('case.servicelevel', string='Service level', track_visibility='onchange')
    casetag_ids = fields.Many2many('case.tag', string='Tags', track_visibility='onchange')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown'),],'Gender', default='unknown', required=True)
    sexorient  = fields.Selection([('homo', 'Homosexual'), ('bi', 'Bisexual'), ('hetero', 'Heterosexual'), ('quest', 'Questioning'), ('unknown', 'Unknown'),],'Sexual Orientation', default='unknown', required=True)
    trans  = fields.Selection([('trans', 'Yes'), ('nottrans', 'No'),('unknown', 'Unknown'),],'Transgender', default='unknown',required=True)
    settlement  = fields.Selection([('budapest', 'Budapest'), ('city', 'Large City'), ('town', 'Smaller settlement'), ('abroad', 'Abroad'), ('unknown', 'Unknown'),],'Settlement', default='unknown',required=True)
    age = fields.Integer('Age', help="Age in years")
    agecateg_id = fields.Many2one('case.agecateg', required=True, string='Age Category')
    demogrtag_ids = fields.Many2many('case.demogrtag', string='Demography Tags')
    activity_count = fields.Integer(compute='_activity_count', string="Activities",)
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['project.task.type'].search([])
        return stage_ids  
                
    @api.one
    def unlink(self):
        tasks = self.env['project.task'].search([('id','=',self.task_id.id)])
        res = super(case_case, self).unlink()
        tasks.unlink()
        return res
    @api.multi
    def _get_code(self):
        self.ensure_one()
        code = ''
        if self.project_id.code: 
            seq_name = 'case.case.' + self.project_id.code.lower()
            if self.env['ir.sequence'].search([('code', '=', seq_name)]):
                code = self.env['ir.sequence'].next_by_code(seq_name)
        return code
class case_servicelevel(models.Model):
    _name = 'case.servicelevel'
    _description = 'Service level'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    sequence = fields.Integer('Sequence', select=True, help='Gives the sequence order when displaying service levels.')
    project_id = fields.Many2one('project.project', 'Service')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the service level without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Service Level has to be unique')
    ]

class case_tag(models.Model):
    _name = 'case.tag'
    _description = 'Case Tags'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    project_id = fields.Many2one('project.project', 'Service')
    parent_id = fields.Many2one('case.tag', 'Parent', ondelete='restrict')
    parent_left = fields.Integer('Parent left', index=True)
    parent_right = fields.Integer('Parent right', index=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Tag has to be unique')
    ]
   
class case_demogrtag(models.Model):
    _name = 'case.demogrtag'
    _description = 'Case Demography Tags'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the demography tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for demography tag has to be unique')
    ]

class case_agecateg(models.Model):
    _name = 'case.agecateg'
    _description = 'Age Category'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the demography tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for age category has to be unique')
    ]
    
class res_partner(models.Model):
    _inherit = ['res.partner']
    serviceuser = fields.Boolean('Service user', help="Check this box if this contact is user of a service.")
    
class project_project(models.Model):
    _inherit = ['project.project']
    code = fields.Char('Code',size=128,required=True)
    service = fields.Boolean('Service', help="Project containing service provision and case management.", default=False)
        
class case_document(models.Model):
    _name = 'case.document'
    _description = 'Case Document'
    _inherits = {
        'ir.attachment': 'document_id',
    }
    document_id = fields.Many2one('ir.attachment', required=True, string='Related Document', ondelete='restrict', help='Document-related data of the case document', auto_join=True)
    date_done = fields.Date('Done Date', select=True, help="Date when the document was created and signed", track_visibility='onchange')
    date = fields.Date('Date', select=True, help="Date of arrival (for incoming) or date of sending (for outgoing)", track_visibility='onchange')
    doctype_id = fields.Many2one('case.doctype', 'Type', select=True, track_visibility='onchange')
    direction = fields.Selection([('in', 'Incoming'), ('out', 'Outgoing'),('local', 'Helyi') ],'Direction', select=True, track_visibility='onchange')
    channel_id = fields.Many2one('docregister.type', 'Channel', select=True, track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Partner', track_visibility='onchange',select=True)
    partner_ids = fields.Many2many('res.partner', string='Other partner(s)', track_visibility='onchange',select=True)
    doc_id = fields.Many2one('docregister.doc', string='Document', track_visibility='onchange',select=True)
    case_id = fields.Many2one('case.case', string='Case', track_visibility='onchange',select=True)
    
class case_doctype(models.Model):
    _name = 'case.doctype'
    _description = 'Case Document Type'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    project_id = fields.Many2one('project.project', 'Service')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Case Document Type has to be unique')
    ]

class project(models.Model):
    _inherit = 'project.task'
    case_ids = fields.One2many('case.case', 'task_id', 'Cases')