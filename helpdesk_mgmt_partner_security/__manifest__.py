# -*- coding: utf-8 -*-
{
    'name': "helpdesk_mgmt_partner_security",

    'summary': """
        Restrict access to partner data to helpdesk team members""",

    'description': """
        Only allow team members to access partner records of ticket partners
    """,

    'author': "Dombos Tamás",
    'license': 'LGPL-3',
    'category': 'Helpdesk',
    'version': '0.1',
    'depends': ['helpdesk_mgmt','contacts'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'security/security.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
