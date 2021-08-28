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

class project_partner_partnerline(models.Model):
    _inherit = ['project_partner.partnerline']
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', ondelete='cascade')

class HelpdeskTicket(models.Model):
    _inherit = ['helpdesk.ticket']
    
    @api.depends('partnerline_ids')
    def _partner_count(self):
        for record in self:
            record.partner_count = len(record.partnerline_ids)
            
    partnerline_ids = fields.One2many('project_partner.partnerline', 'ticket_id', "Partners")
    partner_count = fields.Integer(compute='_partner_count', string="Partners",)
