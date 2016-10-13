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

from openerp.osv import osv
from openerp.osv import fields
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.addons.project import project

            
class case_case(models.Model):
    _name = 'case.case'
    _inherit = ['mail.thread']
    _description = 'Case'
    _inherits = {
        'project.project': 'project_id',
    }
    
    title = fields.Char('Title', select=True)
    project_id = fields.Many2one('project.project', required=True, string='Related Project', ondelete='restrict', help='Project-related data of the case', auto_join=True)
    externalref = fields.Text('External References', track_visibility='onchange')
    description = fields.Html('Description', track_visibility='onchange')
    description_anon = fields.Html('Anonymized Summary')
    servicelevel_ids = fields.Many2many('case.servicelevel', string='Service level', track_visibility='onchange')
    casetag_ids = fields.Many2many('case.tag', string='Tags', track_visibility='onchange')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown'),],'Gender', required=True)
    sexorient  = fields.Selection([('homo', 'Homosexual'), ('bi', 'Bisexual'), ('hetero', 'Heterosexual'), ('quest', 'Questioning'), ('unknown', 'Unknown'),],'Sexual Orientation', required=True)
    trans  = fields.Selection([('trans', 'Yes'), ('nottrans', 'No'),('unknown', 'Unknown'),],'Transgender', required=True)
    settlement  = fields.Selection([('budapest', 'Budapest'), ('city', 'Large City'), ('town', 'Smaller settlement'), ('abroad', 'Abroad'), ('unknown', 'Unknown'),],'Settlement', required=True)
    age = fields.Integer('Age', help="Age in years")
    agecateg_id = fields.Many2one('case.agecateg', required=True, string='Age Category')
    demogrtag_ids = fields.Many2many('case.demogrtag', string='Demography Tags')
    
    state = fields.Selection(
                    [('draft', 'Incoming'), ('open', 'Open'),('close', 'Closed')],
                    string='State', size=16, track_visibility='onchange')
    
    _defaults = {
        'state': 'draft',
        'date_start': None,
        'use_timesheets': 1,
        'use_tasks': 1,
        'gender': 'unknown',
        'sexorient': 'unknown',
        'trans': 'unknown',
        'settlement': 'unknown',

    }
           
    @api.one
    def do_open(self):
        vals={'state': 'open'}
        if not self.code:
            vals['code'] = self._get_code()
        self.write(vals)
        return True
    @api.one
    def do_close(self):
        self.state = 'close'
        return True
    def unlink(self, cr, uid, ids, context=None):
        project_to_delete = set()
        for case in self.browse(cr, uid, ids, context=context):
            if case.project_id:
                project_to_delete.add(case.project_id.id)
        res = super(case_case, self).unlink(cr, uid, ids, context=context)
        self.pool['project.project'].unlink(cr, uid, list(project_to_delete), context=context)
        return res
    @api.multi
    def _get_code(self):
        self.ensure_one()
        code = ''
        if self.department_id.code: 
            seq_name = 'case.case.' + self.department_id.code.lower()
            if self.env['ir.sequence'].search([('code', '=', seq_name)]):
                code = self.env['ir.sequence'].next_by_code(seq_name)
        return code
class case_servicelevel(models.Model):
    _name = 'case.servicelevel'
    _description = 'Service level'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    sequence = fields.Integer('Sequence', select=True, help='Gives the sequence order when displaying service levels.')
    department_id = fields.Many2one('hr.department', 'Department')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the service level without removing it.")
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Service Level has to be unique')
    ]
    _defaults = {
        'active': 1
    }

class case_tag(models.Model):
    _name = 'case.tag'
    _description = 'Case Tags'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    department_id = fields.Many2one('hr.department', 'Department')
    parent_id = fields.Many2one('case.tag', 'Parent', ondelete='restrict')
    parent_left = fields.Integer('Parent left', index=True)
    parent_right = fields.Integer('Parent right', index=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the tag without removing it.")
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Tag has to be unique')
    ]
    _defaults = {
        'active': 1
    }    
class case_demogrtag(models.Model):
    _name = 'case.demogrtag'
    _description = 'Case Demography Tags'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the demography tag without removing it.")
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for demography tag has to be unique')
    ]
    _defaults = {
        'active': 1
    }
class case_agecateg(models.Model):
    _name = 'case.agecateg'
    _description = 'Age Category'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the demography tag without removing it.")
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for age category has to be unique')
    ]
    _defaults = {
        'active': 1
    }
    
class res_partner(models.Model):
    _inherit = ['res.partner']
    serviceuser = fields.Boolean('Service user', help="Check this box if this contact is user of a service.")
    
class hr_department(models.Model):
    _inherit = ['hr.department']
    code = fields.Char('Code',size=128,required=True)
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
    
class case_doctype(models.Model):
    _name = 'case.doctype'
    _description = 'Case Document Type'
    
    name = fields.Char('Name', size=128, required=True, select=True)
    department_id = fields.Many2one('hr.department', 'Department')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the tag without removing it.")
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Case Document Type has to be unique')
    ]
    _defaults = {
        'active': 1
    }  
    
class project(models.Model):
    _inherit = 'project.project'
    case_ids = fields.One2many('case.case', 'project_id', 'Cases')