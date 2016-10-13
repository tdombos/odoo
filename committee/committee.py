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


class committee_committee(models.Model):
    _name = 'committee.committee'
    _inherit = ['mail.thread']
    _description = 'Committee'
    _inherits = {
        'project.project': 'project_id',
    }
    
    @api.depends('meeting_ids')
    def _meeting_count(self):
        for record in self:
            record.meeeting_count = len(record.meeting_ids)
    @api.depends('decision_ids')
    def _decision_count(self):
        for record in self:
            record.decision_count = len(record.decision_ids)
    @api.depends('agendaitem_ids')
    def _agendaitem_count(self):
        for record in self:
            record.agendaitem_count = len(record.agendaitem_ids)
    shortname = fields.Char('Short name', size=64, select=True)
    project_id = fields.Many2one('project.project', required=True, string='Related Project', ondelete='restrict', help='Project-related data of the committee', auto_join=True)
    description = fields.Html('Description', track_visibility='onchange')
    type_ids = fields.Char('Types', size=16, select=True)
    agendaitem_ids = fields.One2many('committee.agendaitem', 'committee_id', 'Agenda Items')
    meeting_ids = fields.One2many('committee.meeting', 'committee_id', 'Meetings')
    decision_ids = fields.One2many('committee.decision', 'committee_id', 'Decisions')
    meeting_count = fields.Integer(compute='_meeting_count', string='Meetings')
    decision_count = fields.Integer(compute='_decision_count', string='Decisions')
    agendaitem_count = fields.Integer(compute='_agendaitem_count', string='Agenda Items')
    
    def unlink(self, cr, uid, ids, context=None):
        project_to_delete = set()
        for committee in self.browse(cr, uid, ids, context=context):
            if committee.project_id:
                project_to_delete.add(committee.project_id.id)
        res = super(committee_committee, self).unlink(cr, uid, ids, context=context)
        self.pool['project.project'].unlink(cr, uid, list(project_to_delete), context=context)
        return res

class committee_meeting(models.Model):
    _name = 'committee.meeting'
    _inherit = ['mail.thread']
    _inherits = {
        'calendar.event': 'meeting_id',
    }
    _description = 'Meeting'

    @api.depends('decision_ids')
    def _decision_count(self):
        for record in self:
            record.decision_count = len(record.decision_ids)

    committee_id = fields.Many2one('committee.committee', 'Committee', required=True, ondelete='restrict',)
    meeting_id = fields.Many2one('calendar.event', 'Event', require=True, ondelete='restrict')
    agendaline_ids = fields.One2many('committee.agendaline', 'meeting_id', string='Agenda')
    decision_ids = fields.One2many('committee.decision', 'meeting_id', 'Decisions')
    decision_count = fields.Integer(compute='_decision_count', string='Decisions')
    state = fields.Selection([
        ('draft', 'Planned'),
        ('open', 'Invitation sent'),
        ('done', 'Held'),
        ('close', 'Memo Done'),
        ('cancel', 'Cancelled')],
        string='State', size=16, readonly=True, track_visibility='onchange')
    
    _defaults = {
        'state': 'draft',
    }
    
    @api.one
    def do_open(self):
        self.state = 'open'
        agendaitems = self.agendaline_ids.mapped('agendaitem_id')
        for agendaitem in agendaitems:
            if agendaitem.state in ('draft','postpone'):
                agendaitem.state = 'open'
        return True
    @api.one
    def do_done(self):
        self.state = 'done'
        agendaitems = self.agendaline_ids.mapped('agendaitem_id')
        for agendaitem in agendaitems:
            if agendaitem.state in ('draft','open'):
                agendaitem.state = 'done'
        return True
    @api.one
    def do_close(self):
        self.state = 'close'
        return True
    @api.one
    def do_cancel(self):
        self.state = 'cancel'
        return True

class calendar_event(models.Model):
    _inherit = 'calendar.event'


class committee_attendance(models.Model):
    _inherit = ['calendar.attendee']
    state = fields.Selection([
        ('needs-action', 'Needs Action'),
        ('tentative', 'Uncertain'),
        ('declined', 'Declined'),
        ('accepted', 'Accepted'),
        ('delegated', 'Delegated'), 
        ('attended', 'Attended')],
        'Status', readonly=True, help="Status of the attendee's participation")
    @api.one
    def do_attend(self):
        self.state = 'attended'
        return True
    
class committee_agendaitem(models.Model):
    _name = 'committee.agendaitem'
    _inherit = ['mail.thread']
    _description = 'Agenda Item'
    
    name = fields.Char('Item Title', size=128, required=True, select=True)
    committee_id = fields.Many2one('committee.committee', 'Committee', required=True)
    notes = fields.Text('Memo')
    decision_ids = fields.One2many('committee.decision', 'agendaitem_id', 'Decisions')
    tag_ids = fields.Many2many('docregister.tag', string='Tag(s)', track_visibility='onchange')
    user_id = fields.Many2one('res.users', 'Assigned to', select=True, track_visibility='onchange')
    description = fields.Text('Description')
    notes = fields.Text('Notes')
    date_deadline = fields.Date('Deadline', select=True, copy=False)
    priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority', select=True)
    state = fields.Selection([
        ('draft', 'Proposed'),
        ('open', 'Scheduled'),
        ('done', 'Closed'),
        ('postpone', 'Postponed'),
        ('cancel', 'Cancelled')],
        string='State', size=16, readonly=True, track_visibility='onchange')
    
    _defaults = {
        'state': 'draft',
    }
    @api.one
    def do_open(self):
        self.state = 'open'
        return True
    @api.one
    def do_done(self):
        self.state = 'done'
        return True
    @api.one
    def do_cancel(self):
        self.state = 'cancel'
        return True
    @api.one
    def do_postpone(self):
        self.state = 'postpone'
        return True
        
class committee_agendaline(models.Model):
    _name = 'committee.agendaline'
    _description = 'Agenda Line'
    
    sequence = fields.Integer('Sequence', select=True, help='Gives the sequence order when displaying a list of tasks.')
    meeting_id  = fields.Many2one('committee.meeting', string='Meeting',required=True)
    agendaitem_id  = fields.Many2one('committee.agendaitem', string='Agenda item',required=True)
    late = fields.Boolean('Late')
    state = fields.Selection(related='agendaitem_id.state',string='State')
    
    @api.one
    def do_postpone(self):
        self.agendaitem_id.state = 'postpone'
        return True
        
class committee_decision(models.Model):
    _name = 'committee.decision'
    _inherit = ['mail.thread']
    _description = 'Decision'

    name = fields.Char('Number', size=128, required=True, select=True)
    agendaitem_id = fields.Many2one('committee.agendaitem', 'Agenda Item')
    committee_id = fields.Many2one('committee.committee', 'Committee', required=True)
    meeting_id = fields.Many2one('committee.meeting', 'Meeting')
    date = fields.Date('Date', required=True)
    partner_ids = fields.Many2many('res.partner', string='People Concerned')
    type_id = fields.Many2one('committee.decisiontype', 'Type')
    text = fields.Text('Text')
    vote = fields.Text('Voting Summary')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Final')],
        string='State', size=16, readonly=True, track_visibility='onchange')

    _sql_constraints = [
        ('name', 'unique(name)', 'Name of Decision Type has to be unique')
    ]
    _defaults = {
        'state': 'draft',
    }
    @api.one
    def do_done(self):
        self.state = 'done'
        return True
    @api.onchange('meeting_id') 
    def set_meetingdata(self):
        if self.meeting_id: 
            self.committee_id = self.meeting_id.committee_id
            self.date = self.meeting_id.start
    @api.onchange('agendaitem_id') 
    def set_agendadata(self):
        if self.agendaitem_id: 
            self.committee_id = self.agendaitem_id.committee_id


class committee_decisiontype(models.Model):
    _name = 'committee.decisiontype'
    _description = 'Decision Type'

    name = fields.Char('Name', size=64, required=True)

    _sql_constraints = [
        ('name', 'unique(name)', 'Name of Decision Type has to be unique')
    ]
    _order = 'name asc'
class project(models.Model):
    _inherit = 'project.project'
    committee_ids = fields.One2many('committee.committee', 'project_id', 'Committees')