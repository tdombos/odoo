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

class HelpdeskTicketAgeCateg(models.Model):
    _name = 'helpdesk.agecateg'
    _description = 'Age Category'
    
    name = fields.Char('Name', size=128, required=True, index=True,translate=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the demography tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for age category has to be unique')
    ]

class HelpdeskTicketDemogrTag(models.Model):
    _name = 'helpdesk.demogrtag'
    _description = 'Ticket Demography Tags'
    
    name = fields.Char('Name', size=128, required=True, index=True)
    active = fields.Boolean('Active', help="If the active field is set to False, it will allow you to hide the demography tag without removing it.", default=True)
    _sql_constraints = [
        ('name', 'unique(name)', 'Name for demography tag has to be unique')
    ]

