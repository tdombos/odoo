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
from openerp import exceptions
from openerp.tools.translate import _
import datetime

class docregister_tag(models.Model):
    _name = "docregister.tag"
    _description = "Tag"
    
    name = fields.Char('Name', size=64, required=True)
    description = fields.Text('Description', help='Detailed description for the tagging label')

    _sql_constraints = [
        ('name', 'unique(name)', 'Tag name has to be unique')
    ]
    _order = 'name asc'
    
class docregister_type(models.Model):
    _name = "docregister.type"
    _description = "Letter Type"

    name  = fields.Char('Name', size=64, required=True)

    _sql_constraints = [
        ('name', 'unique(name)', 'Name of Letter Type has to be unique')
    ]
    _order = 'name asc'
    
class docregister_folder(models.Model):
    """ folder """
    _name = "docregister.folder"
    _description = "Document Folder"
    
    @api.depends('doc_ids')
    def _doc_count(self):
        for record in self:
            record.doc_count = len(record.doc_ids)

    name = fields.Char('Title', size=64, required=True)
    description = fields.Text('Description', help='Description of content and internal organization of folder')
    doc_ids = fields.One2many('docregister.doc', 'folder_id', "Documents")
    doc_count = fields.Integer(compute='_doc_count', string="Documents",)
    state = fields.Selection([('open', 'Active'), ('close', 'Archived')],'State')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the folder without removing it.")
    
    _sql_constraints = [
        ('name', 'unique(name)', 'Foler name has to be unique')
    ]
    _defaults = {
        'state': 'open',
        'active': 1
    }
    _order = 'name asc'
    @api.one
    def folder_close(self):
        self.state = 'close'
        return True
    @api.one
    def folder_open(self):
        self.state = 'open'
        return True
    
class docregister_archivalcateg(models.Model):
    """ doctari tetel"""
    _name = "docregister.archivalcateg"
    _description = "Archival Category"


    code = fields.Char('Code', size=16, required=True)
    name = fields.Char('Name', size=128, required=True)
    description = fields.Text('Description', help='Description for archival category')
    sequence = fields.Integer('Order')
    heading = fields.Boolean('Heading')
    parent_id = fields.Many2one('docregister.archivalcateg', 'Parent', ondelete='restrict')
    parent_left = fields.Integer('Parent left', index=True)
    parent_right = fields.Integer('Parent right', index=True)
    state = fields.Selection([('open', 'Active'),('close', 'Archived')],'State')
    complete_name = fields.Char(compute='compute_complete_name')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the archival category without removing it.")
    
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Archival Category has to be unique')
    ]
    _defaults = {
        'state': 'open',
        'active': 1
    }
    _order = 'sequence'
    @api.one
    def archivalcateg_close(self):
        self.state = 'close'
        return True
    @api.one
    def archivalcateg_open(self):
        self.state = 'open'
        return True

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', '=like', name + "%")] + args,
                               limit=limit)
            if not recs:
                recs = self.search([('name', operator, name)] + args,
                                   limit=limit)
        else:
            recs = self.search(args, limit=limit)
        return recs.name_get()

    @api.one
    def name_get(self):
        return (self.id, self._get_full_name()[0])

    @api.one
    @api.depends('name', 'code')
    def compute_complete_name(self):
        self.complete_name = self._get_full_name()[0]

    @api.one
    def _get_full_name(self):
        if self.code:
            return self.code + ' - ' + self.name
        return self.name
     
class docregister_config_settings(models.TransientModel):
    _name = 'docregister.config.settings'
    _inherit = 'res.config.settings'

    default_reftype = fields.Boolean('Separating in & out',default_model='docregister.config.settings', help ="""Separate reference numbers for incoming & outgoing documents.""")

    
class docregister_doc(models.Model):
    _inherit = ['mail.thread']
    _name = 'docregister.doc'
    _description = "Document"

    register_uid = fields.Many2one('res.users', 'Registered by')
    register_date = fields.Date('Registration Date')
    refcode = fields.Char('Reference Code', size=32, track_visibility='onchange',select=True,copy=False)
    direction = fields.Selection([('in', 'Incoming'), ('out', 'Outgoing')],'Direction', required=True,select=True)
    subject = fields.Char('Subject', size=128, required=True, help="Short summary of the subject of the document", track_visibility='onchange',select=True)
    externalref = fields.Char('External Code', size=128, help="Document reference code used by partner", track_visibility='onchange',select=True)
    partner_id = fields.Many2one('res.partner', string='Primary partner', required=True, track_visibility='onchange',select=True)
    partner_ids = fields.Many2many('res.partner', string='Other partner(s)', required=True, track_visibility='onchange',select=True)
    tag_ids = fields.Many2many('docregister.tag', string='Tag(s)', track_visibility='onchange',select=True)
    archivalcateg_id = fields.Many2one('docregister.archivalcateg', 'Archival Category', select=True, domain=[('heading', '=', False)],track_visibility='onchange')
    date_done = fields.Date('Done Date', select=True, help="Date when the document was created and signed", track_visibility='onchange')
    date = fields.Date('Date',  select=True, required=True, help="Date of arrival (for incoming) or date of sending (for outgoing)", track_visibility='onchange')
    type_id = fields.Many2one('docregister.type', 'Type', required=True, select=True, track_visibility='onchange')
    registered = fields.Selection([('no', 'No'),('registered', 'Registered'),('return', 'Return Receipt')],'Registered Post')
    date_delivery = fields.Date('Delivery Date', help="For letter with Return Receipt: date when letter was delivered", track_visibility='onchange')
    attachmentno = fields.Integer('No. of Attachments', help="Number of documents attached to the main document", track_visibility='onchange')
    predoc_id = fields.Many2one('docregister.doc', 'Preceded by', track_visibility='onchange')
    postdoc_ids = fields.One2many('docregister.doc',  'predoc_id', 'Followed by',readonly=True, track_visibility='onchange')
    basedoc_id = fields.Reference([('committee.meeting','Meeting')],'Base Document')
    user_id = fields.Many2one('res.users', string='Assigned to', select=True, track_visibility='onchange')
    deadline = fields.Date('Deadline', select=True, help="Deadline for dealing with document", track_visibility='onchange')
    folder_id = fields.Many2one('docregister.folder', 'Folder', select=True, track_visibility='onchange')
    folderplace = fields.Char('Within folder', size=64, help="Placement of document within the folder", track_visibility='onchange')
    note = fields.Text('Note', help='Notes related to the document', track_visibility='onchange')
    protected= fields.Boolean('Protected data', help='Document contains protected data', track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'),('open', 'To be answered'),('cancel', 'Deleted'),('fail', 'Postage failed'),('close', 'Closed')],'State', track_visibility='onchange')
        
    _rec_name = 'refcode'
    _defaults = {
        'state': 'draft',
        'registered': 'no',
        'register_uid' : lambda self, cr, uid, ctx:uid,
        'register_date' :  datetime.datetime.now(),
        'protected' : 0
    }
    _sql_constraints = [
        ('refcode', 'unique(refcode)', 'Document Reference Code has to be unique')
    ]
    _order = 'date desc'
    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        res=[]
        for doc in self.browse(cr, uid, ids,context=context):
            if doc.refcode:
                res.append((doc.id, doc.refcode + ' ' + doc.subject))
            else:
                res.append((doc.id, doc.subject))
        return res
    def _get_refcode (self, cr, uid, ids, context={}):
        ir_values = self.pool.get('ir.values')
        reftype = ir_values.get_default(cr, uid,'docregister.config.settings', 'reftype')
        if not reftype:
            refcode = self.pool.get('ir.sequence').get(cr, uid,'doc.mix')
        else:
            if self.direction == 'in':
                refcode = self.pool.get('ir.sequence').get(cr, uid, 'doc.in')
            else:
                refcode = self.pool.get('ir.sequence').get(cr, uid,'doc.out')
        return refcode
    @api.one
    def doc_cancel(self):
        self.state = 'cancel'
        return True
    @api.one
    def doc_fail(self):
        self.state = 'fail'
        return True
    @api.one
    def doc_open(self):
        vals={'state': 'open'}
        if not self.refcode:
            vals['refcode'] = self._get_refcode()
        self.write(vals)
        return True
    @api.one
    def doc_close(self):
        vals={'state': 'close'} 
        if not self.refcode: 
            vals['refcode'] = self._get_refcode()
        self.write(vals)
        return True
    def message_new(self, cr, uid, msg, custom_values=None, context=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        desc=1
        if custom_values is None:
            custom_values = {}
        desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
        defaults = {
            'subject':  msg.get('subject') or _("No Subject"),
            'partner_ids': [(6, 0, msg.get('author_id', False))],
            'date': lambda *a: time.strftime('%Y-%m-%d'),
            'type_id':1, 
            'direction':'in',           
        }
#         if msg.get('author_id'):
#             defaults.update(self.on_change_partner(cr, uid, None, msg.get('author_id'), context=context)['value'])
        
        defaults.update(custom_values)
        return super(docregister_doc, self).message_new(cr, uid, msg, custom_values=defaults, context=context)

class res_partner(models.Model):

    _inherit = "res.partner"

    @api.one
    def _docregister_doc_count(self):
        self.docs_count = self.env['docregister.doc'].search_count(
            [('partner_ids', 'in', self.ids)])

    doc_ids = fields.Many2many(
        'docregister.doc', 'docregister_doc_res_partner_rel', 'docregister_doc_id', 'res_partner_id', string='Registered Documents')
    docs_count = fields.Integer(
        compute="_docregister_doc_count", string="Registered Documents Counts")
