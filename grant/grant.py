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


import logging
logger = logging.getLogger('iktato')
hdlr = logging.FileHandler('/var/tmp/iktato.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

def get_company_currency(self, cr, uid, context=None):
        user_obj = self.pool.get('res.users')
        currency_obj = self.pool.get('res.currency')
        user = user_obj.browse(cr, uid, uid, context=context)
        if user.company_id:
            return user.company_id.currency_id.id
        else:
            return currency_obj.search(cr, uid, [('rate', '=', 1.0)])[0]
            
class grant_fund(models.Model):
    _name = 'grant.fund'
    _inherit = ['mail.thread']
    _description = 'Fund'
    _inherits = {
        'project.project': 'project_id',
    }
    
    @api.depends('report_ids')
    def _report_count(self):
        for record in self:
            record.report_count = len(record.report_ids)
    @api.depends('installment_ids')
    def _installment_calc(self):
        for record in self:
            installments = record.env['grant.installment'].browse(record.installment_ids)
            record.installment_received = len(installments)
            
    project_id = fields.Many2one('project.project', required=True, string='Related Project', ondelete='restrict', help='Project-related data of the fund', auto_join=True)
    members = fields.Many2many('res.partner', string='Project Members', required=True, track_visibility='onchange')
    title = fields.Char('Full title', size=255, select=True, track_visibility='onchange')
    title_orig = fields.Char('Full title (original)', size=255, select=True, track_visibility='onchange')
    type_ids = fields.Char('Types', size=16, select=True)
    proposal_id = fields.Many2one('grant.proposal', string='Proposal', track_visibility='onchange')
    call_id = fields.Many2one('grant.call',string='Call', track_visibility='onchange')
    donor_id = fields.Many2one('res.partner', string='Donor', track_visibility='onchange')
    code_contract = fields.Char('Contract reference', size=64, select=True, track_visibility='onchange')
    categ_ids = fields.Many2many('project.category', string='Tags', track_visibility='onchange')
    fundcurrency_id = fields.Many2one('res.currency', string='Currency', required=True, track_visibility='onchange')
    amount_requested = fields.Float(related='proposal_id.amount_requested', readonly=True, track_visibility='onchange')
    amount_granted = fields.Float(string='Amount granted', track_visibility='onchange')
    cofinannce = fields.Float(string='Financial cofinancing', track_visibility='onchange')
    cofinannce_inkind = fields.Float(string='Inkind cofinancing', track_visibility='onchange')
    report_ids = fields.One2many('grant.report', 'fund_id', "Reports")
    installment_ids = fields.One2many('grant.installment', 'fund_id', "Installments")
    report_count = fields.Integer(compute='_report_count', string="Reports no",)
    installment_received = fields.Integer(compute='_installment_calc', string="Money received",)
    state = fields.Selection(
                    [('draft', 'Contracting'), ('open', 'Implementation'), ('done', 'Reporting'),('cancel', 'Failed'),('close', 'Closed')],
                    string='State', size=16, readonly=True, track_visibility='onchange')
    
    _defaults = {
        'state': 'draft',
        'fundcurrency_id': get_company_currency,
        'date_start': None,
        'use_timesheets': 1
    }
    @api.onchange('proposal_id') 
    def change_proposal(self):
        self.donor_id = self.proposal_id.donor_id
        self.call_id = self.proposal_id.call_id
        self.amount_requested = self.proposal_id.amount_requested
        self.fundcurrency_id = self.proposal_id.currency_id
    @api.one
    def do_open(self):
        self.state = 'open'
        return True
    @api.one
    def do_done(self):
        self.state = 'done'
        return True
    @api.one
    def do_close(self):
        self.state = 'close'
        return True
    @api.one
    def do_cancel(self):
        self.state = 'cancel'
        return True
        
class grant_proposal(models.Model):
    _name = 'grant.proposal'
    _inherit = ['mail.thread']
    _description = 'Proposal'
    
    name = fields.Char('Title', size=128, required=True, track_visibility='onchange')
    title = fields.Char('Full title', size=255, select=True, track_visibility='onchange')
    call_id = fields.Many2one('grant.call', string='Call', track_visibility='onchange')
    donor_id = fields.Many2one('res.partner', string='Donor', track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='Responsible', track_visibility='onchange')
    coordinator_id = fields.Many2one('res.partner', string='Coordinator', track_visibility='onchange')
    partner_ids = fields.Many2many('res.partner', string='Partners', track_visibility='onchange')
    code_proposal = fields.Char('Proposal reference', size=64, select=True, track_visibility='onchange')
    categ_ids = fields.Many2many('project.category', string='Tags', track_visibility='onchange')
    description = fields.Text('Description', track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, track_visibility='onchange')
    amount_requested = fields.Float(string='Amount requested', track_visibility='onchange')
    cofinannce = fields.Float(string='Financial cofinancing', track_visibility='onchange')
    cofinannce_inkind = fields.Float(string='Inkind cofinancing', track_visibility='onchange')
    date_submitted = fields.Date('Submitted', track_visibility='onchange')
    date_decision = fields.Date('Decision expected', track_visibility='onchange')
    date_start = fields.Date('Expected start', track_visibility='onchange')
    date = fields.Date('Expected end', track_visibility='onchange')
    state = fields.Selection(
                    [('draft', 'Idea'), ('open', 'Submitted'),('cancel', 'Not submitted'),('done', 'Won'),('close', 'Lost')],
                    string='State', size=16, readonly=True, track_visibility='onchange')
    
    _defaults = {
        'state': 'draft',
        'currency_id': get_company_currency,
        'date_start': None
    }
    @api.onchange('call_id') 
    def set_calldata(self):
        self.donor_id = self.call_id.donor_id
        self.date_decision = self.call_id.date_decision
    @api.one
    def do_open(self):
        self.state = 'open'
        return True
    @api.one
    def do_done(self):
        self.state = 'done'
        return True
    @api.one
    def do_close(self):
        self.state = 'close'
        return True
    @api.one
    def do_cancel(self):
        self.state = 'cancel'
        return True
    @api.multi
    def createfund(self):
        self.ensure_one() 
        Fund = self.env['grant.fund']
        new = Fund.create({
            'name':self.name,
            'donor_id':self.donor_id.id,
            'title_orig':self.title,
            'call_id':self.call_id.id,
            'proposal_id':self.id,
            'description':self.description,
            'date':self.date,
            'date_start':self.date_start,
            'fundcurrency_id':self.currency_id.id
        })
        if self.coordinator_id:
            ProjectPartner = self.env['project_partner.partnerline']
            role = self.env.ref('grant.grant_role_coordinator')
            new2 = ProjectPartner.create({
                'partner_id':self.coordinator_id.id,
                'project_id':new.project_id.id,
                'role_id':role.id
            })
        view_id = self.env.ref('grant.view_grant_fund_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Funds'),
            'res_model': 'grant.fund',
            'res_id': new.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
        
class grant_call(models.Model):
    _name = 'grant.call'
    _inherit = ['mail.thread']
    _description = 'Call'
    
    name = fields.Char('Title', size=128, required=True, track_visibility='onchange')
    code = fields.Char('Call no.', size=128, track_visibility='onchange')
    donor_id = fields.Many2one('res.partner', string='Donor', track_visibility='onchange')
    date = fields.Datetime(string="Deadline", track_visibility='onchange')
    categ_ids = fields.Many2many('project.category', string='Tags', track_visibility='onchange')
    description = fields.Text('Description', track_visibility='onchange')
    url = fields.Char('Link', size=255)
    date_decision = fields.Date('Decision expected', track_visibility='onchange')
    state = fields.Selection(
       [('draft', 'Planned'), ('open', 'Open'), ('close', 'Expired'),('cancel', 'Cancelled')],
       string='State', size=16, track_visibility='onchange')
    
    _defaults = {
        'state': 'open',
    }
    @api.one
    def do_open(self):
        self.state = 'open'
        return True
    @api.one
    def do_close(self):
        self.state = 'close'
        return True
    @api.one
    def do_cancel(self):
        self.state = 'cancel'
        return True

class grant_report(models.Model):
    _name = 'grant.report'
    _inherit = ['mail.thread']
    _description = 'Report'
   
    name = fields.Char('Name', size=128, required=True, track_visibility='onchange')
    fund_id = fields.Many2one('grant.fund', string='Fund', required=True)
    date_open = fields.Date('From', track_visibility='onchange')
    date_close = fields.Date('To', track_visibility='onchange')
    date_due = fields.Date('Report due', track_visibility='onchange')
    date_submit = fields.Date('Submitted on', track_visibility='onchange')
    type = fields.Selection([('interim', 'Interim'),('final', 'Final')], 'Type')
    reportcontent_id = fields.Many2many('grant.reportcontent', string='Report content', track_visibility='onchange')
    state = fields.Selection(
       [('draft', 'Scheduled'), ('open', 'Submitted'), ('revise', 'Revision'), ('close', 'Accepted')],
       string='State', size=16, readonly=True, track_visibility='onchange')
    
    _defaults = {
        'state': 'draft',
    }
    @api.one
    def do_open(self):
        self.state = 'open'
        return True
    @api.one
    def do_close(self):
        self.state = 'close'
        return True
    @api.one
    def do_revise(self):
        self.state = 'revise'
        return True
class grant_reportcontent(models.Model):
    _name = 'grant.reportcontent'
    _description = 'Report content'
   
    name = fields.Char('Name', size=64, required=True, track_visibility='onchange')
    _sql_constraints = [
        ('name', 'unique(name)', 'Name of Decision Type has to be unique')
    ]
    _order = 'name asc'
    
class grant_installment(models.Model):
    _name = 'grant.installment'
    _inherit = ['mail.thread']
    _description = 'Installment'

    name = fields.Char('Name', size=128, required=True)
    fund_id = fields.Many2one('grant.fund', string='Fund', required=True,)
    date_expected = fields.Date('Date expected', track_visibility='onchange')
    date_received = fields.Date('Date received', track_visibility='onchange')
    amount_expected = fields.Float(string='Amount expected', track_visibility='onchange')
    amount_received = fields.Float(string='Amount received', track_visibility='onchange')
    fundcurrency_id = fields.Many2one(related='fund_id.fundcurrency_id', readonly=True, track_visibility='onchange')
    currency_id = fields.Many2one(related='fund_id.currency_id', readonly=True)
    amount_received_local = fields.Float(string='Amount received (company currency)', track_visibility='onchange')
    state = fields.Selection(
       [('draft', 'Scheduled'), ('done', 'Received'),('cancel', 'Cancelled'),  ],
       string='State', size=16, readonly=True, track_visibility='onchange')

    _defaults = {
        'state': 'draft',
    }
    @api.one
    def do_done(self):
        self.state = 'done'
        return True
    @api.one
    def do_cancel(self):
        self.state = 'cancel'
        return True
class res_partner(models.Model):
    _inherit = ['res.partner']
    donor = fields.Boolean('Donor', help="Check this box if this contact is a donor.")
    