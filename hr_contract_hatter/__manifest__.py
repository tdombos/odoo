# -*- coding: utf-8 -*-
{
    'name': "Hatter customizations to hr_contract",

    'summary': """
        Add main contract, add reference to paper signed contract""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Tamás Dombos",
    'website': "https://hatter.hu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_contract', 'docregister'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
