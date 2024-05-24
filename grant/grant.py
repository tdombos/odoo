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

def get_company_currency(self):
    return self.env.ref('base.main_company').currency_id

class grant_call(models.Model):
    _name = 'grant.call'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Call'
    
    @api.depends('proposal_ids')
    def _proposal_count(self):
        for record in self:
            record.proposal_count = len(record.proposal_ids)
    
    name = fields.Char('Title', size=128, required=True, tracking=True)
    code = fields.Char('Call no.', size=128, tracking=True)
    donor_id = fields.Many2one('res.partner', string='Donor', tracking=True)
    date_start = fields.Datetime(string="Open date", tracking=True)
    date = fields.Datetime(string="Deadline", tracking=True)
    tag_ids = fields.Many2many('project.tags', string='Tags', tracking=True)
    description = fields.Text('Description', tracking=True)
    url = fields.Char('Link', size=255)
    date_decision = fields.Date('Decision expected', tracking=True)
    min_amount = fields.Float(string='Minimum amount', tracking=True)
    max_amount = fields.Float(string='Maximum amount', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, tracking=True,default=get_company_currency)
    proposal_ids = fields.One2many('grant.proposal', 'call_id', "Proposals")
    proposal_count = fields.Integer(compute='_proposal_count', string="Proposals no",)
    direction = fields.Selection(
       [('in', 'Incoming'), ('out', 'Outgoing')],
       string='Direction', tracking=True,required=True)
    state = fields.Selection(
       [('draft', 'Planned'), ('open', 'Open'), ('close', 'Expired'),('cancel', 'Cancelled')],
       string='State', tracking=True,default='open')

    def do_open(self):
        self.ensure_one()
        self.state = 'open'
        return True
    def do_close(self):
        self.ensure_one()
        self.state = 'close'
        return True
    def do_cancel(self):
        self.ensure_one()
        self.state = 'cancel'
        return True
    def _expire_grant(self):
        for rec in self.search([('state', '=', 'open')]):
            if rec.date and rec.date < fields.Datetime.now():
                rec.state ='close'

class grant_proposal(models.Model):
    _name = 'grant.proposal'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Proposal'
    
    name = fields.Char('Title', size=128, required=True, tracking=True)
    title = fields.Char('Full title', size=255, tracking=True)
    call_id = fields.Many2one('grant.call', string='Call', tracking=True)
    fund_ids = fields.One2many('grant.fund', 'proposal_id', "Funds")
    donor_id = fields.Many2one('res.partner', string='Donor', tracking=True)
    user_id = fields.Many2one('res.users', string='Responsible', tracking=True)
    applicant_id = fields.Many2one('res.partner', string='Applicant', tracking=True)
    applicant_contact_id = fields.Many2one('res.partner', string='Applicant contact', tracking=True)
    partner_ids = fields.Many2many('res.partner', string='Partners', tracking=True)
    code_proposal = fields.Char('Proposal reference', size=64, tracking=True)
    tag_ids = fields.Many2many('project.tags', string='Tags', tracking=True)
    description = fields.Html('Description', tracking=True)
    comment = fields.Html(string='Notes')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, tracking=True,default=get_company_currency)
    amount_requested = fields.Float(string='Amount requested', tracking=True)
    cofinannce = fields.Float(string='Financial cofinancing', tracking=True)
    cofinannce_inkind = fields.Float(string='Inkind cofinancing', tracking=True)
    date_submitted = fields.Date('Submitted', tracking=True)
    date_decision = fields.Date('Decision expected', tracking=True)
    date_start = fields.Date('Expected start', tracking=True)
    date = fields.Date('Expected end', tracking=True)
    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        domain=[("res_model", "=", "grant.proposal")],
        string="Attachments",
    )
    direction = fields.Selection(
       [('in', 'Incoming'), ('out', 'Outgoing')],
       string='Direction', tracking=True,required=True)   
    state = fields.Selection(
                    [('draft', 'Idea'), ('open', 'Submitted'),('cancel', 'Not submitted'),('done', 'Won'),('close', 'Lost')],
                    string='State', tracking=True,default='draft', group_expand='_expand_states')
    def _expand_states(self, states, domain, order):
        incoming = self._context.get('incoming', False)
        if (incoming):
            return ['open', 'done', 'close']
        else:
            return [key for key, val in type(self).state.selection]
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code_proposal", "/") == "/":
                vals["code_proposal"] = self._prepare_proposal_code(vals)
        return super().create(vals_list)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        res = super().copy(default)
        return res
    def _prepare_proposal_code(self, values):
        seq = self.env["ir.sequence"]
        if "company_id" in values:
            seq = seq.with_company(values["company_id"])
        return seq.next_by_code("grant.proposal.sequence") or "/"
    @api.onchange('call_id') 
    def set_calldata(self):
        self.donor_id = self.call_id.donor_id
        self.date_decision = self.call_id.date_decision
        self.direction = self.call_id.direction
    def do_open(self):
        self.ensure_one()
        self.state = 'open'
        if (not self.date_submitted): 
            self.date_submitted = fields.Date.today()
        return True
    def do_done(self):
        self.ensure_one()
        self.state = 'done'
        return True
    def do_close(self):
        self.ensure_one()
        self.state = 'close'
        return True
    def do_cancel(self):
        self.ensure_one()
        self.state = 'cancel'
        return True
    def createfund(self):
        self.ensure_one() 
        Fund = self.env['grant.fund']
        new = Fund.create({
            'name':self.name,
            'donor_id':self.donor_id.id,
            'title':self.title,
            'title_orig':self.title,
            'call_id':self.call_id.id,
            'proposal_id':self.id,
            'description':self.description,
            'date':self.date,
            'date_start':self.date_start,
            'direction':self.direction,
            'partner_id':self.applicant_contact_id.id,
            'fundcurrency_id':self.currency_id.id
        })
        if self.applicant_id:
            ProjectPartner = self.env['project_partner.partnerline']
            role = self.env.ref('grant.grant_role_applicant')
            new2 = ProjectPartner.create({
                'partner_id':self.applicant_id.id,
                'project_id':new.project_id.id,
                'role_id':role.id
            })
        for partner in self.partner_ids:
            ProjectPartner = self.env['project_partner.partnerline']
            role = self.env.ref('grant.grant_role_partner')
            new2 = ProjectPartner.create({
                'partner_id':partner.id,
                'project_id':new.project_id.id,
                'role_id':role.id
            })
        view_id = self.env.ref('grant.view_grant_fund_form').id
        for follower in self.message_follower_ids:
            new.message_subscribe(partner_ids=follower.partner_id.ids, subtype_ids=follower.subtype_ids.ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Funds',
            'res_model': 'grant.fund',
            'res_id': new.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'nodestroy': True,
        }

class grant_fund(models.Model):
    _name = 'grant.fund'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Fund'
    _inherits = {
        'project.project': 'project_id',
    }
    
    @api.depends('requirement_ids')
    def _requirement_count(self):
        for record in self:
            record.requirement_count = len(record.requirement_ids)
    @api.depends('analytic_account_id')
    def _get_installments(self):
        for record in self:
            record.installment_ids = record.env['account.move'].search([('analytic_account_id', '=', record.analytic_account_id.id)]) 
    @api.depends('installment_ids')
    def _installment_calc(self):
        for record in self:
            installments = record.env['account.move'].search([('analytic_account_id', '=', record.analytic_account_id.id)]) 
            record.installment_received = len(installments)
            
    project_id = fields.Many2one('project.project', required=True, string='Related Project', ondelete='restrict', help='Project-related data of the fund', auto_join=True)
    members = fields.Many2many('res.partner', string='Project Members', required=True, tracking=True)
    title = fields.Char('Full title', size=255, tracking=True)
    title_orig = fields.Char('Full title (original)', size=255, tracking=True)
    description = fields.Html('Description', 
    #tracking=True
    )
    fundtype_id = fields.Many2one('grant.fundtype', required=True, string='Fund Type', ondelete='restrict', help='Type of fund')
    proposal_id = fields.Many2one('grant.proposal', string='Proposal', tracking=True)
    call_id = fields.Many2one('grant.call',string='Call', related='proposal_id.call_id', readonly=True, tracking=True)
    donor_id = fields.Many2one('res.partner', string='Donor', tracking=True)
    code_contract = fields.Char('Contract reference', size=64, tracking=True)
    tag_ids = fields.Many2many('project.tags', string='Tags', tracking=True)
    fundcurrency_id = fields.Many2one('res.currency', string='Currency', required=True, tracking=True,default=get_company_currency)
    amount_requested = fields.Float(related='proposal_id.amount_requested', readonly=True, tracking=True)
    amount_granted = fields.Float(string='Amount granted', tracking=True)
    cofinannce = fields.Float(string='Financial cofinancing', tracking=True)
    cofinannce_inkind = fields.Float(string='Inkind cofinancing', tracking=True)
    direction = fields.Selection(
       [('in', 'Incoming'), ('out', 'Outgoing')],
       string='Direction', tracking=True,required=True) 
    requirement_ids = fields.One2many('grant.requirement', 'fund_id', "Requirements")
    installment_ids = fields.One2many('account.move', compute='_get_installments', string="Installments")
    requirement_count = fields.Integer(compute='_requirement_count', string="Requirements no",)
    installment_received = fields.Integer(compute='_installment_calc', string="Money received",)
    incoming_journal_id = fields.Many2one(related='fundtype_id.incoming_journal_id')
    outgoing_journal_id = fields.Many2one(related='fundtype_id.outgoing_journal_id')
    state = fields.Selection(
                    [('draft', 'Contracting'), ('open', 'Implementation'), ('done', 'Reporting'),('cancel', 'Failed'),('close', 'Closed')],
                    string='State', tracking=True,default='draft')
    
    _defaults = {
        'date_start': None,
        'use_timesheets': 1
    }
    @api.onchange('proposal_id') 
    def change_proposal(self):
        self.donor_id = self.proposal_id.donor_id
        self.amount_requested = self.proposal_id.amount_requested
        self.fundcurrency_id = self.proposal_id.currency_id
    def do_open(self):
        self.ensure_one()
        self.state = 'open'
        return True
    def do_done(self):
        self.ensure_one()
        self.state = 'done'
        return True
    def do_close(self):
        self.ensure_one()
        self.state = 'close'
        return True
    def do_cancel(self):
        self.ensure_one()
        self.state = 'cancel'
        return True

class grant_requirement(models.Model):
    _name = 'grant.requirement'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Requirement'
   
    name = fields.Char('Name', size=128, required=True, tracking=True)
    fund_id = fields.Many2one('grant.fund', string='Fund', required=True)
    commercial_partner_id = fields.Many2one('res.partner',string='Customer', related='fund_id.commercial_partner_id', readonly=True, tracking=True)
    date_open = fields.Date('From', tracking=True)
    date_close = fields.Date('To', tracking=True)
    date_due = fields.Date('Requirement due', tracking=True)
    date_submit = fields.Date('Submitted on', tracking=True)
    type = fields.Selection([('contract', 'Contract'),('interim', 'Interim'),('final', 'Final')], 'Type')
    reportcontent_ids = fields.Many2many('grant.reportcontent', string='Report content', tracking=True)
    user_id = fields.Many2one(related='fund_id.user_id', readonly=True)
    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        domain=[("res_model", "=", "grant.requirement")],
        string="Attachments",
    )
    state = fields.Selection(
       [('draft', 'Scheduled'), ('open', 'Due'), ('done', 'Submitted'), ('revise', 'Revision'), ('close', 'Accepted')],
       string='State', readonly=True, tracking=True,default='draft')
    def name_get(self):
        res = []
        for requirement in self:
            name = requirement.name
            if requirement.fund_id:
                name = requirement.fund_id.name + ' - ' + name
            res.append((requirement.id, name))
        return res
    def do_open(self):
        self.ensure_one()
        self.state = 'open'
        return True
    def do_done(self):
        self.ensure_one()
        self.state = 'done'
        if (not self.date_submit): 
            self.date_submit = fields.Date.today()
        return True
    def do_close(self):
        self.ensure_one()
        self.state = 'close'
        return True
    def do_revise(self):
        self.ensure_one()
        self.state = 'revise'
        return True
    def _open_requirement_date(self):
        for rec in self.search([('state', '=', 'draft')]):
            if rec.date_close and rec.date_close < fields.Date.today():
                rec.state ='open'

class grant_reportcontent(models.Model):
    _name = 'grant.reportcontent'
    _description = 'Report content'
   
    name = fields.Char('Name', size=64, required=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name of Report content has to be unique')
    ]
    _order = 'name asc'

class AccountMove(models.Model):
    _inherit = ['account.move']
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", copy=False, ondelete='set null',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", check_company=True,
        help="Analytic account to which this move and all it's lines are linked for financial management. ")
    requirement_id = fields.Many2one('grant.requirement', string="Requirement", ondelete='set null',
        help="Requirement on which the payment is contingent on. ")
    installment = fields.Boolean(string="Grant installment")

class grant_fundtype(models.Model):
    _name = "grant.fundtype"
    _description = "Fund Type"

    name  = fields.Char('Name', size=64, required=True)
    incoming_journal_id = fields.Many2one('account.journal', string='Icoming Grant Journal', required=True)
    outgoing_journal_id = fields.Many2one('account.journal', string='Outgoing Grant Journal', required=True)
    
    _sql_constraints = [
        ('name', 'unique(name)', 'Name of Letter Type has to be unique')
    ]
    _order = 'name asc'
    
class res_partner(models.Model):
    _inherit = ['res.partner']
    donor = fields.Boolean('Donor', help="Check this box if this contact is a donor.")
    
class Project(models.Model):
    _inherit = ['project.project']
    fund_ids = fields.One2many('grant.fund', 'project_id', string='Funds', auto_join=True)
    commercial_partner_id = fields.Many2one(related="partner_id.commercial_partner_id")