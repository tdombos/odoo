from odoo.http import route, request
from odoo.addons.portal.controllers import portal
from odoo.tools import plaintext2html
from odoo.exceptions import AccessError, MissingError
from datetime import date
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
            domain = []
            count = request.env["grant.proposal"].search_count(domain)
            values["grant_proposals_count"] = count
        if "grant_funds_count" in counters:
            domain = []
            count = request.env["grant.fund"].search_count(domain)
            values["grant_funds_count"] = count
        return values

    @route(["/my/proposals", "/my/proposals/page/<int:page>"], auth="user", website=True)
    def my_proposals(self, page=1, **kw):
        Proposal = request.env["grant.proposal"]
        domain = [["direction","=","in"]]
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
        ["/my/funds", "/my/funds/page/<int:page>"],
        auth="user",
        website=True,
    )
    def my_funds(self, page=1, **kw):
        Fund = request.env["grant.fund"]
        domain = [["direction","=","in"]]
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
                "page_name": "grant-funds",
                "default_url": "/my/funds",
                "pager": pager_data,
            }
        )
        return request.render("grant_portal.my_grant_funds", values)

    @route(["/my/proposals/<int:proposal_id>"], auth="user", website=True)
    def portal_my_proposal(self, proposal_id=None, access_token=None, **kw):
        try:
            proposal_sudo = self._document_check_access(
                "grant.proposal", proposal_id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        for attachment in proposal_sudo.attachment_ids:
            attachment.generate_access_token()
        return request.render("grant_portal.proposal", {"doc": proposal_sudo, "page_name": "proposal"})

    @route(["/my/funds/<int:fund_id>"], auth="user", website=True)
    def portal_my_fund(self, fund_id=None, access_token=None, **kw):
        try:
            fund_sudo = self._document_check_access(
                "grant.fund", fund_id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        return request.render("grant_portal.fund", {"doc": fund_sudo, "page_name": "fund"})
    @route(["/my/requirements/<int:requirement_id>"], auth="user", website=True)
    def portal_my_requirement(self, requirement_id=None, access_token=None, **kw):
        try:
            requirement_sudo = self._document_check_access(
                "grant.requirement", requirement_id, access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        for attachment in requirement_sudo.attachment_ids:
            attachment.generate_access_token()
        return request.render("grant_portal.requirement", {"doc": requirement_sudo, "page_name": "requirement"})    
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
                    [("email", "=", kw.get("company_email"))], order="create_date desc", limit=1
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
                    [("email", "=", kw.get("partner_email"))], order="create_date desc", limit=1
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
    @http.route("/requirement/submit", type="http", auth="user")
    def requirement_submit(self, **kw):
        """Submit requirement"""
        values = {}
        for field_name, field_value in kw.items():
            if field_name.endswith("_id"):
                values[field_name] = int(field_value)
            else:
                values[field_name] = field_value
        requirement = (
            http.request.env["grant.requirement"]
            .sudo()
            .search([("id", "=", values["requirement_id"])])
        )
        requirement.ensure_one() 
        requirement.state = 'done'
        requirement.date_submit = date.today()
        return werkzeug.utils.redirect("/my/requirements/" + str(requirement.id))
