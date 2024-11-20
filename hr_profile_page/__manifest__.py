{
    'name': "Profile page",
    'version': '17.0.1.0.0',
    'depends': ['website', 'hr'],
    'author': "Miklos Dombos",
    'category': 'Employees',
    'description': "Profile page for employees with categories",
    'data': [
        'views/editor.xml',
        'views/filters.xml',
        'views/snippet.xml',
    ],
    'assets': {
            'web.assets_frontend': [
                'hr_profile_page/static/js/controller.js',
                'hr_profile_page/static/scss/styles.scss'
            ],
        },
    "application": False,
    "installable": True,
    "auto_install": False,
    "license":"Other proprietary",
}