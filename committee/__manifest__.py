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


{
    'name': 'Committee',
    'version': '14.0.0.1',
    'category': 'Office management',
    'description': 'Managing committees, meetings, agendas and decisions',
    'author': 'Dombos Tamás',
    'license': 'LGPL-3',
    'website': '',
    'depends': ['project', 'calendar', 'docregister'],
    'data': ['security/ir.model.access.csv',
     'committee_view.xml'
     #, 'committee_data.xml'
    ], 
    'demo': [],
    'test':[],
    'installable': True,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
