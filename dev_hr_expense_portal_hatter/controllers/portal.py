from odoo import fields, http, _
from odoo.http import route, request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from datetime import datetime, date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
from odoo.addons.portal.controllers.mail import _message_post_helper
import werkzeug
from odoo.osv.expression import OR
import base64

class CustomerPortal(CustomerPortal):
    
    @http.route(['/my/hr_expense', '/my/hr_expense/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_expense(self, page=1, date_begin=None, date_end=None, sortby=None,filterby=None,groupby='none',search=None,search_in='content', **kw):
        values = self._prepare_portal_layout_values()
        expense_id = request.env['hr.expense']
        domain = [
             ('employee_id.user_id', '=',request.env.user.id)
        ]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name desc'},
			'product_id': {'label': _('Product'), 'order': 'product_id desc'},
        }

        # default sortby order
        if not sortby:
            sortby = 'name'
		
        today = fields.Date.today()
        this_week_end_date = fields.Date.to_string(fields.Date.from_string(today) + timedelta(days=7))
        week_ago = datetime.today() - timedelta(days=7)
        month_ago = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d %H:%M:%S')
        starting_of_year = datetime.now().date().replace(month=1, day=1)    
        ending_of_year = datetime.now().date().replace(month=12, day=31)

        def sd(date):
        	return fields.Datetime.to_string(date)
        def previous_week_range(date):
        	start_date = date + timedelta(-date.weekday(), weeks=-1)
        	end_date = date + timedelta(-date.weekday() - 1)
        	return {'start_date':start_date.strftime('%Y-%m-%d %H:%M:%S'), 'end_date':end_date.strftime('%Y-%m-%d %H:%M:%S')}
		
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'today': {'label': _('Today'), 'domain': [('date', '>=', datetime.strftime(date.today(),'%Y-%m-%d 00:00:00')),('date', '<=', datetime.strftime(date.today(),'%Y-%m-%d 23:59:59'))]},
            'yesterday':{'label': _('Yesterday'), 'domain': [('date', '>=', datetime.strftime(date.today() - timedelta(days=1),'%Y-%m-%d 00:00:00')),('date', '<=', datetime.strftime(date.today(),'%Y-%m-%d 23:59:59'))]},
            'week': {'label': _('This Week'),
                     'domain': [('date', '>=', sd(datetime.today() + relativedelta(days=-today.weekday()))), ('date', '<=', this_week_end_date)]},
            'last_seven_days':{'label':_('Last 7 Days'),
                         'domain': [('date', '>=', sd(week_ago)), ('date', '<=', sd(datetime.today()))]},
            'last_week':{'label':_('Last Week'),
                         'domain': [('date', '>=', previous_week_range(datetime.today()).get('start_date')), ('date', '<=', previous_week_range(datetime.today()).get('end_date'))]},
            
            'last_month':{'label':_('Last 30 Days'),
                         'domain': [('date', '>=', month_ago), ('date', '<=', sd(datetime.today()))]},
            'month':{'label': _('This Month'),
                    'domain': [
                       ("date", ">=", sd(today.replace(day=1))),
                       ("date", "<", (today.replace(day=1) + relativedelta(months=1)).strftime('%Y-%m-%d 00:00:00'))
                    ]
                },
            'year':{'label': _('This Year'),
                    'domain': [
                       ("date", ">=", sd(starting_of_year)),
                       ("date", "<=", sd(ending_of_year)),
                    ]
                }
        }

		
        if not filterby:
        	filterby = 'all'
        domain += searchbar_filters[filterby]['domain'] 

        sort_order = searchbar_sortings[sortby]['order']
	
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('All')},
            'product_id': {'input': 'product_id', 'label': _('Product')},
            # 'account_id': {'input': 'account_id', 'label': _('Account')},
            'analytic_account_id': {'input': 'analytic_account_id', 'label': _('Analytic')},
            'state': {'input': 'state', 'label': _('State')},
            
        }
        
        # count for pager
        exp_count = expense_id.search_count(domain)



        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in Name')},
            'product': {'input': 'product', 'label': _('Search in Product')},
			'state': {'input': 'state', 'label': _('Search in State')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }

		# search
        if search and search_in:
        	search_domain = []
        	if search_in in ('name', 'all'):
        		search_domain = OR([search_domain, [('name', 'ilike', search)]])
        	if search_in in ('product', 'all'):
        		search_domain = OR([search_domain, [('product_id', 'ilike', search)]])
        	if search_in in ('state', 'all'):
        		search_domain = OR([search_domain, [('state', 'ilike', search)]])
        	domain += search_domain
        
        # make pager
        pager = portal_pager(
            url="/my/hr_expense",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby,'search_in': search_in,'search': search},
            total=exp_count,
            page=page,
            step=self._items_per_page
        )
        expense = expense_id.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_contact_history'] = expense.ids[:100] 
	
        if groupby == 'product_id':
        	grouped_expense = [request.env['hr.expense'].concat(*g) for k, g in groupbyelem(expense, itemgetter('product_id'))]
        elif groupby == 'account_id':
        	grouped_expense = [request.env['hr.expense'].concat(*g) for k, g in groupbyelem(expense, itemgetter('account_id'))]
        elif groupby == 'analytic_account_id':
        	grouped_expense = [request.env['hr.expense'].concat(*g) for k, g in groupbyelem(expense, itemgetter('analytic_account_id'))]
        elif groupby == 'state':
        	grouped_expense = [request.env['hr.expense'].concat(*g) for k, g in groupbyelem(expense, itemgetter('state'))]
        else:
        	grouped_expense = [expense]
        
        product_id = request.env['product.product'].sudo().search([('can_be_expensed','=',True)])
        fund_id = request.env['grant.fund'].search([])
        analytic_account_id = request.env['account.analytic.account']
        for fund in fund_id:
            analytic_account_id = analytic_account_id | fund.project_id.analytic_account_id

        values.update({
            'date': date_begin,
            'expense': expense.sudo(),
            'page_name': 'expense_tree',
			'grouped_expense': grouped_expense,
            'pager': pager,
            'default_url': '/my/hr_expense',
			'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
			'searchbar_inputs': searchbar_inputs,
			'search_in': search_in,
			'search': search,
			'searchbar_sortings': searchbar_sortings,
			'searchbar_groupby':searchbar_groupby,
            'page_name': 'expense_tree',
			'filterby': filterby,
            'sortby': sortby,
            'groupby': groupby,
			'product_ids':product_id,
            'analytic_account_ids':analytic_account_id,


        })
        return request.render("dev_hr_expense_portal.portal_my_expense", values)

    @http.route(['/dev_expense/expense_create'], type='http', auth="public", methods=['POST'], website=True)
    def expense_submit(self, **post):
        cr, uid, context, pool = http.request.cr, http.request.uid, http.request.context, request.env
        product_id = request.env['product.product'].sudo().browse(int(post['product_id']))
        analytic_account_id = request.env['account.analytic.account'].sudo().browse(int(post['analytic_account_id']))
        employee_id = request.env['hr.employee'].sudo().search([('user_id','=',request.env.user.id)]).id
        expense_id = pool['hr.expense'].sudo().create({
            'name':post['name'],
            'product_id':product_id and product_id.id ,
            'product_uom_id':product_id.uom_id and product_id.uom_id.id or False ,
            'total_amount':post['amount'],
            'unit_amount':post['unit_amount'],
            'quantity':post['quantity'],
            'reference':post['bill_reference'],
            'payment_mode':post['payment_mode'],
            'payment_online':post['payment_online'],
            'partner_name':post['partner_name'],
            'partner_email':post['partner_email'],
            'partner_tax':post['partner_tax'],
            'employee_id':employee_id,
            'product_id':product_id and product_id.id ,
            'analytic_account_id':analytic_account_id and analytic_account_id.id ,
        })
        if expense_id:
            if post['expense_file']:
                attachment={
                            'name':post['name'],
                            'datas': base64.b64encode(post['expense_file'].read()),
                            'res_model':'hr.expense',
                            'type':'binary',
                            'res_id':expense_id.id,
                }
                attachment_id = request.env['ir.attachment'].sudo().create(attachment)
            url = expense_id.get_portal_url()
            return werkzeug.utils.redirect(url) 