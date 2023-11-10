from odoo.http import route, request
from odoo.addons.portal.controllers import portal
from odoo.tools import plaintext2html
import odoo.http as http
import base64
import logging
import datetime
import werkzeug
_logger = logging.getLogger(__name__)

class CustomerPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "grant_proposals_count" in counters:
            count = request.env["grant.proposal"].search_count([])
            values["grant_proposals_count"] = count
        return values
        if "grant_funds_count" in counters:
            count = request.env["grant.fund"].search_count([])
            values["grant_funds_count"] = count
        return values
    @route(
        ["/my/proposals", "/my/proposals/page/<int:page>"],
        auth="user",
        website=True,
    )
    def my_proposals(self, page=1, **kw):
        Proposal = request.env["grant.proposal"]
        domain = []
        # Prepare pager data
        proposal_count = Proposal.search_count(domain)
        pager_data = portal.pager(
            url="/my/proposals",
            total=proposal_count,
            page=page,
            step=self._items_per_page,
        )
        # Recordset according to pager and domain filter
        proposals = Proposal.search(
            domain, limit=self._items_per_page, offset=pager_data["offset"]
        )
        # Prepare template values
        values = self._prepare_portal_layout_values()
        values.update(
            {
                "proposals": proposals,
                "page_name": "grant-proposals",
                "default_url": "/my/proposals",
                "pager": pager_data,
            }
        )
        return request.render("grant_portal.my_grant_proposals", values)

    @route(
        ["/my/funds", "/my/proposals/page/<int:page>"],
        auth="user",
        website=True,
    )
    def my_funds(self, page=1, **kw):
        Fund = request.env["grant.fund"]
        domain = []
        # Prepare pager data
        fund_count = Fund.search_count(domain)
        pager_data = portal.pager(
            url="/my/funds",
            total=fund_count,
            page=page,
            step=self._items_per_page,
        )
        # Recordset according to pager and domain filter
        funds = Fund.search(
            domain, limit=self._items_per_page, offset=pager_data["offset"]
        )
        # Prepare template values
        values = self._prepare_portal_layout_values()
        values.update(
            {
                "funds": funds,
                "page_name": "grant-proposals",
                "default_url": "/my/proposals",
                "pager": pager_data,
            }
        )
        return request.render("grant_portal.my_grant_funds", values)

    @route(["/my/proposals/<model('grant.proposal'):doc>"], auth="user", website=True)
    def portal_my_project(self, doc=None, **kw):
        return request.render("grant_portal.proposal", {"doc": doc})

    @route(["/my/funds/<model('grant.fund'):doc>"], auth="user", website=True)
    def portal_my_project(self, doc=None, **kw):
        return request.render("grant_portal.fund", {"doc": doc})
    
    @route(["/calls/apply/<model('grant.call'):call>"], auth="user", website=True)
    def calls_apply(self, call, **kwargs):
        error = {}
        default = {}
        if 'grant_portal_error' in request.session:
            error = request.session.pop('grant_portal_error_error')
            default = request.session.pop('grant_portal_error_default')
        return request.render("grant_portal.apply", {
            'call': call,
            'error': error,
            'default': default,
        })

    def _prepare_submit_proposal_vals(self, **kw):
        vals = {
            "description": plaintext2html(kw.get("description")),
            "name": kw.get("title"),
            "title": kw.get("title"),
            "amount_requested": kw.get("amount_requested"),
            "call_id": kw.get("call_id"),
            "state": 'open',
            "code_proposal": '/',
            "direction": 'in',
            "date_submitted": datetime.date.today()
        }
        if kw.get("company_email"):
            applicant = (
                http.request.env["res.partner"]
                .sudo()
                .search(
                    [("email", "=", kw.get("company_email"))]
                )
            )
            if not applicant: 
                if kw.get("company")==kw.get("partner_name"):
                    is_company = False,
                else: 
                    is_company = True
                applicant = request.env["res.partner"].sudo().create(
                        {
                            "name": kw.get("company"),
                            "email": kw.get("company_email"),
                            "is_company": is_company,
                        }
                    )
            vals.update({"applicant_id": applicant.id})
        if kw.get("call_id"):
            call = (http.request.env["grant.call"]
                .sudo()
                .search(
                    [("id", "=", kw.get("call_id"))]
                )
            )
            if call: 
                vals.update({"date_decision": call.date_decision, "donor_id": call.donor_id.id})
        if kw.get("partner_email") == request.env.user.partner_id.email:
            vals.update({"applicant_contact_id": request.env.user.partner_id.id})
        else:
            applicant_contact = (
                http.request.env["res.partner"]
                .sudo()
                .search(
                    [("email", "=", kw.get("partner_email"))]
                )
            )
            if not applicant_contact: 
                applicant_contact = request.env["res.partner"].sudo().create(
                        {
                            "name": kw.get("partner_name"),
                            "email": kw.get("partner_email"),
                        }
                    )
            vals.update({"applicant_contact_id": applicant_contact.id})
        return vals

    @route("/submitted/proposal", type="http", auth="user", website=True, csrf=True)
    def submit_proposal(self, **kw):
        _logger.debug("NANU")
        vals = self._prepare_submit_proposal_vals(**kw)
        new_proposal = request.env["grant.proposal"].sudo().create(vals)
        new_proposal.message_subscribe(partner_ids=request.env.user.partner_id.ids)
        if kw.get("proposal"):
            for c_file in request.httprequest.files.getlist("proposal"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "grant.proposal",
                            "res_id": new_proposal.id,
                        }
                    )
        if kw.get("budget"):
            for c_file in request.httprequest.files.getlist("budget"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "grant.proposal",
                            "res_id": new_proposal.id,
                        }
                    )
        return werkzeug.utils.redirect("/my/proposals/%s" % new_proposal.id)
