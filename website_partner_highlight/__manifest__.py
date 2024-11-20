{
    'name': "Partner highlight",
    'version': '17.0.1.0.0',
    'depends': ['website_partner'],
    'author': "Miklos Dombos",
    'category': 'Website/Customizations',
    'description': "",
    'data': [
        'views/snippet.xml',
        'views/editor.xml',
    ],
    'assets': {
                'web.assets_frontend': [
                    'website_partner_highlight/static/js/controller.js'
                ],
            },
    "application": False,
    "installable": True,
    "auto_install": False,
    "license":"Other proprietary",
}