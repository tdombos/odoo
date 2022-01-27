# -*- coding: utf-8 -*-
{
    'name': "Import Files",

    'summary': """
        Import files """,

    'description': """
        Long description of module's purpose
    """,

    'author': "KABEER KB and Tamas Dombos",
    'website': "",
    'price':"",
    'currency':'EUR',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Documents',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/import_attachment_view.xml',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    # "external_dependencies": {
    # 'python': ['magic']

# },
'installable':True
}
