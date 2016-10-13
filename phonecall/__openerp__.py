# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY Odoo S.A. <http://www.odoo.com>
#    @author Paramjit Singh A. Sahota <sahotaparamjitsingh@gmail.com>
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
    'name': 'Phonecalls',
    'version': '8.0.1.0.0',
    'author': 'Dombos Tamas',
    'category': 'Office',
    'description': """
Phone Calls
============================
Log incoming and outgoing calls.
    """,
    'data': [
        'crm_phonecall_to_phonecall_view.xml',
        'crm_phonecall_view.xml',
        'crm_phonecall_menu.xml',
        # 'report/crm_phonecall_report_view.xml',
    ],
    'demo': [],
    'depends': ['crm','mail'],
    'installable': True,
}
