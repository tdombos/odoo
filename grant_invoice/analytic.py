# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv
from openerp.osv import fields

class account_analytic_line(osv.osv):
    _inherit = 'account.analytic.line'

    _columns = {
        'deferred_invoice_line_id': fields.many2one('account.invoice.line', 'Invoice Line', readonly=True),
        'deferred_invoice_id': fields.related('deferred_invoice_line_id', 'invoice_id', type="many2one",
            relation="account.invoice", string="Invoice", store=False, readonly=True),
        'deferred_account_move_line_id': fields.many2one('account.move.line', 'Account Entry Line', readonly=True),
        'deferred_account_move_id': fields.related('deferred_account_move_line_id', 'move_id', type="many2one",
            relation="account.move", string="Account Entry", store=False, readonly=True),
        }
