# -*- coding: utf-8 -*-
{
    'name': "Google Docs Merge",

    'summary': """
        Merge a template created in Google Docs with odoo fields""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Tamas Dombos",
    'license': 'LGPL-3',
    'website': "https://hatter.hu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['google_drive'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/google_drive_data.xml',
        # 'views/res_config_settings_views.xml'
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
