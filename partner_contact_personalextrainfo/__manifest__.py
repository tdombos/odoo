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

{
    "name": "Extra Personal Info",
    "version": "8.0.1.0.0",
    "author": "Dombos Tamás",
    'license': 'LGPL-3',
    "category": "Customer Relationship Management",
    "website": "https://odoo-community.org/",
    "depends": [
        'partner_contact_personal_information_page'
    ],
    "data": [
        "views/res_partner.xml",
    ],
}
