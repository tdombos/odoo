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

class HelpdeskTicket(models.Model):
    _inherit =  'helpdesk.ticket'
    @api.depends('activity_ids')
    def _activity_count(self):
        for record in self:
            record.activity_count = self.env['mail.activity'].with_context(active_test=False).search_count(['&',('res_id', 'in', self.ids),('res_model', '=', 'helpdesk.ticket')])
    def _compute_attached_docs_count(self):
        Doc = self.env['helpdesk.document']
        for ticket in self:
            ticket.doc_count = Doc.search_count([
               ('ticket_id', '=', ticket.id)
            ])
    def _default_agecat (self):
        return self.env.ref('helpdesk_mgmt_hatter_demogr.helpdesk_agecateg_unknown').id

    @api.depends('partnerline_ids')
    def _partner_count(self):
        for record in self:
            record.partner_count = len(record.partnerline_ids)
    start_date= fields.Datetime(string='Ticket arrived',
        default='',
        index=True, copy=False)
    externalref = fields.Text('External References', tracking=True)
    description_anon = fields.Html('Anonymized Summary')
    servicelevel_ids = fields.Many2many('helpdesk.servicelevel', string='Service level', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('unknown', 'Unknown'),],'Gender', default='unknown', required=True)
    sexorient  = fields.Selection([('homo', 'Homosexual'), ('bi', 'Bisexual'), ('hetero', 'Heterosexual'), ('quest', 'Questioning'), ('unknown', 'Unknown'),],'Sexual Orientation', default='unknown', required=True)
    trans  = fields.Selection([('trans', 'Yes'), ('nottrans', 'No'),('unknown', 'Unknown'),],'Transgender', default='unknown',required=True)
    settlement  = fields.Selection([('budapest', 'Budapest'), ('city', 'Large City'), ('town', 'Smaller settlement'), ('abroad', 'Abroad'), ('unknown', 'Unknown'),],'Settlement', default='unknown',required=True)
    age = fields.Integer('Age', help="Age in years")
    agecateg_id = fields.Many2one('helpdesk.agecateg', required=True, string='Age Category', default=_default_agecat)
    demogrtag_ids = fields.Many2many('helpdesk.demogrtag', string='Demography Tags')
    activity_count = fields.Integer(compute='_activity_count', string="Activities",)
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    partnerline_ids = fields.One2many('project_partner.partnerline', 'ticket_id', "Partners")
    partner_count = fields.Integer(compute='_partner_count', string="Partners",)
    complete_name = fields.Char(compute='compute_complete_name')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("number", "/") == "/":
                team = self.env['helpdesk.ticket.team'].browse(vals.get("team_id"))
                if team: 
                    seq_name = 'helpdesk.ticket.' + team.code.lower()
                    vals["number"] = self.env["ir.sequence"].next_by_code(seq_name)
        return super().create(vals_list)
    _rec_name = 'complete_name'
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('number', operator, name)] + args,
                               limit=limit)
            if not recs:
                recs = self.search([('name', operator, name)] + args,
                                   limit=limit)
        else:
            recs = self.search(args, limit=limit)
        return recs.name_get()

    @api.depends('name', 'number')
    def compute_complete_name(self):
        for ticket in self:
            if ticket.number:
                ticket.complete_name = ticket.number + ' - ' + ticket.name
            else:
                ticket.complete_name = ticket.name
class HelpdeskTicketServiceLevel(models.Model):
    _name = 'helpdesk.servicelevel'
    _description = 'Service level'
    
    name = fields.Char('Name', size=128, required=True, index=True)
    sequence = fields.Integer('Sequence', index=True, help='Gives the sequence order when displaying service levels.')
    team_id = fields.Many2one('helpdesk.ticket.team', 'Team')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the service level without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Service Level has to be unique')
    ]

class HelpdeskTicketTag(models.Model):
    _inherit = 'helpdesk.ticket.tag'
    team_id = fields.Many2one('helpdesk.ticket.team', 'Team')
    parent_id = fields.Many2one(
        'helpdesk.ticket.tag',
        string='Parent Tag',
        ondelete='restrict',
        index=True)
    child_ids = fields.One2many( 
        'helpdesk.ticket.tag', 'parent_id',
        string='Child Tags')
    parent_path = fields.Char(index=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Tag has to be unique')
    ]
    _parent_store = True
    _parent_name = "parent_id" 

    # @api.constraints('parent_id')
    # def _check_hierarchy(self):
        # if not self._check_recursion():
            # raise models.ValidationError('Error! You cannot create recursive categories.')

class ResPartner(models.Model):
    _inherit = ['res.partner']
    serviceuser = fields.Boolean('Service user', help="Check this box if this contact is user of a service.")
	
class ResPartner(models.Model):
    _inherit = ['res.partner']
    serviceuser = fields.Boolean('Helpdesk client', help="Check this box if this contact is client of a helpdesk.")

class HelpdeskTeam(models.Model):
    _inherit = ['helpdesk.ticket.team']
    code = fields.Char('Code', size=16, required=True, index=True)
    
class project_partner_partnerline(models.Model):
    _inherit = ['project_partner.partnerline']
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', ondelete='cascade')

class HelpdeskTicketDocument(models.Model):
    _name = 'helpdesk.document'
    _description = 'Ticket Document'
    _inherits = {
        'ir.attachment': 'document_id',
    }
    document_id = fields.Many2one('ir.attachment', required=True, string='Related Document', ondelete='restrict', help='Document-related data of the ticket document', auto_join=True)
    date_done = fields.Date('Done Date', index=True, help="Date when the document was created and signed")
    date = fields.Date('Date', index=True, help="Date of arrival (for incoming) or date of sending (for outgoing)")
    doctype_id = fields.Many2one('helpdesk.doctype', 'Type', index=True)
    direction = fields.Selection([('in', 'Incoming'), ('out', 'Outgoing'),('local', 'Helyi') ],'Direction', index=True)
    channel_id = fields.Many2one('docregister.type', 'Channel', index=True)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True)
    partner_ids = fields.Many2many('res.partner', string='Other partner(s)', index=True)
    doc_id = fields.Many2one('docregister.doc', string='Document', index=True)
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket',index=True)
    filename = fields.Char(compute='compute_filename')
    
    api.depends('name', 'date_done')
    def compute_filename(self):
        for doc in self:
            if doc.date_done:
                doc.filename = doc.date_done.strftime("%Y-%m-%d") + ' ' + doc.name
            else:
                doc.filename = doc.name
    
    
    
    
class HelpdeskTicketDocType(models.Model):
    _name = 'helpdesk.doctype'
    _description = 'Helpdesk Document Type'
    
    name = fields.Char('Name', size=128, required=True, index=True)
    team_id = fields.Many2one('helpdesk.ticket.team', 'Team')
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for Helpdesk Document Type has to be unique')
    ]
