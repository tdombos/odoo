{
    'name': 'Hatter.hu Theme',
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
        'views/website_employee_templates.xml',
    ],
    'images': [
        'static/description/hatter_poster.jpg',
        'static/description/hatter_screenshot.png',
    ],
    'snippet_lists': {
        'homepage': ['s_banner', 's_references', 's_text_image', 's_color_blocks_2', 's_images_wall'],
    },
    'license': 'LGPL-3',
    'assets': {
        'website.assets_wysiwyg': [
            'website_blog/static/src/snippets/s_blog_posts/options.js',
        ],
        'website.assets_editor': [
            'theme_hatterhu/static/src/js/tour.js',
        ],
    }
}
