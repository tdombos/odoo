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



class Committee(models.Model):
    _name = 'committee.committee'
    _description = 'Committee'
    _inherits = {
        'project.project': 'project_id',
    }
    _inherit = ['mail.thread','mail.activity.mixin']
    @api.depends('meeting_ids')
    def _meeting_count(self):
        for record in self:
            record.meeting_count = len(record.meeting_ids)
    @api.depends('decision_ids')
    def _decision_count(self):
        for record in self:
            record.decision_count = len(record.decision_ids)
    shortname = fields.Char('Short name', size=64, select=True)
    project_id = fields.Many2one('project.project', required=True, string='Related Project', ondelete='restrict', help='Project-related data of the committee', auto_join=True)
    meeting_ids = fields.One2many('calendar.event', 'committee_id', 'Meetings')
    decision_ids = fields.One2many('committee.decision', 'committee_id', 'Decisions')
    meeting_count = fields.Integer(compute='_meeting_count', string='Meetings')
    decision_count = fields.Integer(compute='_decision_count', string='Decisions')

class Meeting(models.Model):
    _inherit = ['calendar.event']

    @api.depends('decision_ids')
    def _decision_count(self):
        for record in self:
            record.decision_count = len(record.decision_ids)

    committee_id = fields.Many2one('committee.committee', 'Committee', ondelete='restrict',)
    decision_ids = fields.One2many('committee.decision', 'meeting_id', 'Decisions')
    decision_count = fields.Integer(compute='_decision_count', string='Decisions')
    state = fields.Selection([
        ('draft', 'Planned'),
        ('open', 'Invitation sent'),
        ('done', 'Held'),
        ('close', 'Memo Done'),
        ('cancel', 'Cancelled')],
        string='State', group_expand='_expand_states', default='draft', size=16, track_visibility='onchange')

    _order = 'start desc'
    @api.model
    def _get_public_fields(self):
        return self._get_recurrent_fields() | self._get_time_fields() | self._get_custom_fields() | {
            'id', 'active', 'allday',
            'duration', 'user_id', 'interval',
            'count', 'rrule', 'recurrence_id', 'show_as','state','committee_id'}
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
        
class Attendee(models.Model):
    _inherit = ['calendar.attendee']
    state = fields.Selection(selection_add=[('attended', 'Attended')])
    def do_attend(self):
        """ Records if the person attended the meeting. """
        return self.write({'state': 'attended'})
    
class CommitteeDecision(models.Model):
    _name = 'committee.decision'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Decision'

    name = fields.Char('Number', size=128, required=True, select=True)
    committee_id = fields.Many2one('committee.committee', 'Committee', required=True)
    meeting_id = fields.Many2one('calendar.event', 'Meeting')
    date = fields.Date('Date', required=True)
    partner_ids = fields.Many2many('res.partner', string='People Concerned')
    type_id = fields.Many2one('committee.decisiontype', 'Type')
    text = fields.Text('Text')
    vote = fields.Text('Voting Summary')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Final')],
        string='State', default='draft', group_expand='_expand_states', size=16, track_visibility='onchange')

    _sql_constraints = [
        ('name', 'unique(name)', 'Name of Decision Type has to be unique')
    ]
    _order = 'date desc'
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]
    def do_done(self):
        return self.write({'state': 'done'})
    @api.onchange('meeting_id') 
    def set_meetingdata(self):
        if self.meeting_id: 
            self.committee_id = self.meeting_id.committee_id
            self.date = self.meeting_id.start

class CommitteeDecisionType(models.Model):
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