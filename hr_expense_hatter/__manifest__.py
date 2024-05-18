# -*- coding: utf-8 -*-
{
    'name': "Háttér customizations to hr_expense",

    'summary': """
        Introduce overview of expenses reported, extend payment modes.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Tamás Dombos",
    'license': 'LGPL-3',
    'website': "https://hatter.hu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_expense'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
