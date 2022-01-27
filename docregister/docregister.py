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
from odoo.exceptions import ValidationError
from odoo import _

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
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the folder without removing it.", default=True)

    _sql_constraints = [
        ('name', 'unique(name)', 'Foler name has to be unique')
    ]
    _order = 'name asc'

    def folder_close(self):
        self.ensure_one()
        self.state = 'close'
        return True

    def folder_open(self):
        self.ensure_one()
        self.state = 'open'
        return True

class docregister_archivalcateg(models.Model):
    """ doctari tetel"""
    _name = "docregister.archivalcateg"
    _description = "Archival Category"


    code = fields.Char('Code', size=16, required=True)
    name = fields.Char('Name', size=128, required=True)
    description = fields.Text('Description', help='Description for archival category')
    sequence = fields.Integer(default=10,
        help="Gives the sequence of this category when displaying the category list.")
    heading = fields.Boolean('Heading')
    parent_id = fields.Many2one('docregister.archivalcateg', 'Parent', ondelete='restrict')
    parent_left  = fields.Integer('Parent left', index=True)
    parent_right = fields.Integer('Parent right', index=True)
    complete_name = fields.Char(compute='compute_complete_name')
    retentiontime = fields.Integer('Retention time (years)')
    nondesposable = heading = fields.Boolean('Non-disposable')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the archival category without removing it.",default=True)

    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Archival Category has to be unique')
    ]

    _order = 'sequence'
    _rec_name = 'complete_name'
    def archivalcateg_close(self):
        self.ensure_one()
        self.state = 'close'
        return True

    def archivalcateg_open(self):
        self.ensure_one()
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

    @api.depends('name', 'code')
    def compute_complete_name(self):
        for categ in self:
            if categ.code:
                categ.complete_name = categ.code + ' - ' + categ.name
            else:
                categ.complete_name = categ.name

class docregister_doc(models.Model):
    _inherit = ['mail.thread','mail.activity.mixin']
    _name = 'docregister.doc'
    _description = "Document"

    register_uid = fields.Many2one('res.users', 'Registered by', default=lambda self: self.env.uid)
    register_date = fields.Date('Registration Date',default=datetime.date.today())
    refcode = fields.Char('Reference Code', size=32, track_visibility='onchange',select=True,copy=False)
    direction = fields.Selection([('in', 'Incoming'), ('out', 'Outgoing')],'Direction', select=True)
    subject = fields.Char('Subject', size=128, required=True, help="Short summary of the subject of the document", track_visibility='onchange',select=True)
    externalref = fields.Char('External Code', size=128, help="Document reference code used by partner", track_visibility='onchange',select=True)
    partner_id = fields.Many2one('res.partner', string='Primary partner', track_visibility='onchange',select=True)
    partner_ids = fields.Many2many('res.partner', string='Other partner(s)', track_visibility='onchange')
    tag_ids = fields.Many2many('docregister.tag', string='Tag(s)', track_visibility='onchange',select=True)
    archivalcateg_id = fields.Many2one('docregister.archivalcateg', 'Archival Category', select=True, domain=[('heading', '=', False)],track_visibility='onchange')
    date_done = fields.Date('Done Date', select=True, help="Date when the document was created and signed", track_visibility='onchange')
    date = fields.Date('Date',  select=True, required=True, help="Date of arrival (for incoming) or date of sending (for outgoing)", track_visibility='onchange')
    type_id = fields.Many2one('docregister.type', 'Type', select=True, track_visibility='onchange')
    registered = fields.Selection([('no', 'No'),('registered', 'Registered'),('return', 'Return Receipt')],'Registered Post', default='no')
    date_delivery = fields.Date('Delivery Date', help="For letter with Return Receipt: date when letter was delivered", track_visibility='onchange')
    attachmentno = fields.Integer('No. of Attachments', help="Number of documents attached to the main document", track_visibility='onchange')
    predoc_id = fields.Many2one('docregister.doc', 'Preceded by', track_visibility='onchange')
    postdoc_ids = fields.One2many('docregister.doc',  'predoc_id', 'Followed by',readonly=True, track_visibility='onchange')
    basedoc_id = fields.Reference([('calendar.event','Meeting')],'Base Document')
    user_id = fields.Many2one('res.users', string='Assigned to', select=True, track_visibility='onchange')
    deadline = fields.Date('Deadline', select=True, help="Deadline for dealing with document", track_visibility='onchange')
    folder_id = fields.Many2one('docregister.folder', 'Folder', select=True, track_visibility='onchange')
    folderplace = fields.Char('Within folder', size=64, help="Placement of document within the folder", track_visibility='onchange')
    note = fields.Text('Note', help='Notes related to the document', track_visibility='onchange')
    protected= fields.Boolean('Protected data', help='Document contains protected data', track_visibility='onchange', default=False)
    state = fields.Selection([('draft', 'Draft'),('open', 'To be answered'),('fail', 'Postage failed'),('close', 'Closed')],'State', default='draft', track_visibility='onchange')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the document without removing it.",default=True)

    _rec_name = 'refcode'

    @api.constrains('date_done')
    def _check_date_done(self):
        for record in self:
            if record.date_done > fields.Date.today():
                raise ValidationError(_("The done date cannot be set in the future"))

    _sql_constraints = [
        ('refcode', 'unique(refcode)', 'Document Reference Code has to be unique')
    ]
    _order = 'date desc'

    def name_get(self):
        res = []
        for doc in self:
            if doc.refcode:
                res.append((doc.id, doc.refcode + ' ' + doc.subject))
            else:
                res.append((doc.id, doc.subject))
        return res

    def _get_refcode (self):
        reftype = False
        if not reftype:
            refcode = self.env['ir.sequence'].with_context(ir_sequence_date=self.date).next_by_code('docregister.doc.mix')
        else:
            if self.direction == 'in':
                refcode = self.env['ir.sequence'].next_by_code('docregister.doc.in')
            else:
                refcode = self.env['ir.sequence'].next_by_code('docregister.doc.out')
        return refcode

    def doc_fail(self):
        self.ensure_one()
        self.state = 'fail'
        return True

    def doc_open(self):
        self.ensure_one()
        vals={'state': 'open'}
        if not self.refcode:
            vals['refcode'] = self._get_refcode()
        self.write(vals)
        return True

    def doc_close(self):
        self.ensure_one()
        vals={'state': 'close'} 
        if not self.refcode: 
            vals['refcode'] = self._get_refcode()
        self.write(vals)
        return True
    # def message_new(self, cr, uid, msg, custom_values=None, context=None):
        # """ Overrides mail_thread message_new that is called by the mailgateway
            # through message_process.
            # This override updates the document according to the email.
        # """
        # desc=1
        # if custom_values is None:
            # custom_values = {}
        # desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
        # defaults = {
            # 'subject':  msg.get('subject') or _("No Subject"),
            # 'partner_ids': [(6, 0, msg.get('author_id', False))],
            # 'date': lambda *a: time.strftime('%Y-%m-%d'),
            # 'type_id':1, 
            # 'direction':'in',           
        # }
# #         if msg.get('author_id'):
# #             defaults.update(self.on_change_partner(cr, uid, None, msg.get('author_id'), context=context)['value'])
        
        # defaults.update(custom_values)
        # return super(docregister_doc, self).message_new(cr, uid, msg, custom_values=defaults, context=context)

class res_partner(models.Model):

    _inherit = "res.partner"

    def _docregister_doc_count(self):
        for record in self:
            record.doc_count = self.env['docregister.doc'].search_count(['|',('partner_id', 'in', self.ids),('partner_ids', 'in', self.ids)])

#   doc_ids = fields.Many2many('docregister.doc', 'docregister_doc_res_partner_rel', 'docregister_doc_id', 'res_partner_id', string='Registered Documents')
    doc_count = fields.Integer(compute="_docregister_doc_count", string="Registered Documents Counts", compute_sudo=True)
