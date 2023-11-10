# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import urls

from odoo import api, fields, models, _
from odoo.tools.translate import html_translate
from odoo.exceptions import UserError


class Call(models.Model):

    _name = 'grant.call'
    _inherit = ['grant.call', 'website.seo.metadata', 'website.published.multi.mixin']

    def _get_default_website_description(self):
        default_description = self.env.ref("grant_portal.default_website_description", raise_if_not_found=False)
        return (default_description._render() if default_description else "")

    website_published = fields.Boolean(help='Set if the call is published on the website of the company.')
    website_description = fields.Html('Website description', translate=html_translate, sanitize_attributes=False, default=_get_default_website_description, prefetch=False, sanitize_form=False)

    def _compute_website_url(self):
        super(Call, self)._compute_website_url()
        for call in self:
            call.website_url = "/calls/detail/%s" % call.id

    def set_open(self):
        self.write({'website_published': False})
        return super(Call, self).set_open()

    def get_backend_menu_id(self):
        return self.env.ref('grant.menu_grant').id