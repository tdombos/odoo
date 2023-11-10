{
    'name': 'Bring-In Theme',
    'description': 'Theme for Hatter.hu',
    'category': 'Theme/Corporate',
    'summary': '',
    'sequence': 110,
    'version': '1.0.0',
    'author': 'Dombos Miklós',
    'depends': ['website'],
    'data': [
        'data/ir_asset.xml',
        'views/images.xml',
        'views/customizations.xml',
    ],
    'images': [
        'static/description/bringin_poster.jpg',
        'static/description/bringin_screenshot.png',
    ],
    'snippet_lists': {
        'homepage': ['s_banner', 's_references', 's_text_image', 's_color_blocks_2', 's_images_wall'],
    },
    'license': 'LGPL-3',
    'assets': {
        'website.assets_editor': [
            'theme_bringin/static/src/js/tour.js',
        ],
        'website.assets_wysiwyg': [
            'theme_bringin/static/src/xml/web_editor_fontsizes.xml'
    ],
    }
}
