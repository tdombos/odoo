# -*- coding: utf-8 -*-

# Odoo, Open Source Management Solution
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp import _, api, fields, models
import logging


_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    # ID Number
    passportnumber = fields.Char('Passport Number', track_visibility='onchange')
    idnumber = fields.Char('ID Number', track_visibility='onchange')
    socsecnumber = fields.Char('Social Security Number', select=True, track_visibility='onchange')
    personaltaxnumber = fields.Char('Personl Tax Number', size=16, track_visibility='onchange')
    mothername = fields.Char("Mother's Name", track_visibility='onchange')
    birthplace = fields.Char('Place of Birth', track_visibility='onchange')
    fullname = fields.Char('Full Name', track_visibility='onchange')
    birthname = fields.Char('Birth Name', track_visibility='onchange')
    
