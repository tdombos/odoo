{
    'name': 'Custom Page Background',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Add custom background image for each website page',
    'depends': ['website'],
    'data': [
        'views/view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_page_background/static/scss/styles.scss',
        ],
    },
}