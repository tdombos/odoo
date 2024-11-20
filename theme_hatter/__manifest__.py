{
    'name': 'Theme Háttér',
    'description': 'Theme for hatter.hu',
    'category': 'Theme',
    'sequence': 10,
    'version': '1.0',
    'depends': ['website'],
    'data': [
        'views/header.xml',
        'views/blog.xml',
        'views/cards.xml',
        'data/shapes.xml',
        'views/shapes.xml',
    ],
    'assets':{
            'web.assets_frontend': [
                'theme_hatter/static/src/scss/styles.scss'
            ],
            'web._assets_primary_variables': [
                "theme_hatter/static/src/scss/primary_variables.scss",
            ]
    },
    'images': [
    ],
    'snippet_lists': {
    },
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}