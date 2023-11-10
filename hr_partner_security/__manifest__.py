# -*- coding: utf-8 -*-
{
    'name': "hr_partner_security",

    'summary': """
        Restrict access to partner data to department members""",

    'description': """
        Only allow employees sharing a department with employee to access home partner records of the employee
    """,

    'author': "Dombos Tamás",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HR',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'security/security.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
