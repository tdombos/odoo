from odoo import models


class ThemeBringin(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_bringin_post_copy(self, mod):
        self.enable_asset('Ripple effect SCSS')
        self.enable_asset('Ripple effect JS')
        self.enable_header_off_canvas()
