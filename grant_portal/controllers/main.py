from odoo import http
from odoo.http import request


class Main(http.Controller):

    @http.route("/calls", auth="public", website=True)
    def catalog(self, **kwargs):
        Call = http.request.env["grant.call"]
        # List calls available to current UID
        domain = [('state', '=', 'open')] + request.website.website_domain()
        call_ids = Call.search(domain, order="is_published desc").ids
        # Browse calls as superuser, because address is restricted
        calls = Call.sudo().browse(call_ids)
        res =  http.request.render(
            "grant_portal.grant_calls",
            {"calls": calls, "expired": False},
        )
        return res
    @http.route("/calls/expired", auth="public", website=True)
    def catalog_expired(self, **kwargs):
        Call = http.request.env["grant.call"]
        # List calls available to current UID
        domain = [('state', 'in', ('close','cancel'))] + request.website.website_domain()
        call_ids = Call.search(domain, order="is_published desc").ids
        # Browse calls as superuser, because address is restricted
        calls = Call.sudo().browse(call_ids)
        res =  http.request.render(
            "grant_portal.grant_calls",
            {"calls": calls, "expired": True},
        )
        return res
    @http.route('''/calls/detail/<model("grant.call"):call>''', type='http', auth="public", website=True, sitemap=True)
    def calls_detail(self, call, **kwargs):
        return request.render("grant_portal.detail", {
            'call': call,
            'main_object': call,
        })