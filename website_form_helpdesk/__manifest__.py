# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Online Ticket Submission',
    'category': 'Website/Website',
    'summary': 'Add a ticket form to your website',
    'version': '1.0',
    'description': """
Generate tickets in Helpdesk app from a form published on your website.
    """,
    'depends': ['website', 'helpdesk_mgmt'],
    'data': [
        'data/website_form_helpdesk_data.xml',
        ],
    'installable': True,
    'auto_install': True,
    'assets': {
        'website.assets_editor': [
            'website_form_helpdesk/static/src/**/*',
        ],
    },
    'license': 'LGPL-3',
}
