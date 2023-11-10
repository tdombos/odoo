# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class helpdesk_mgmt_partner_security(models.Model):
#     _name = 'helpdesk_mgmt_partner_security.helpdesk_mgmt_partner_security'
#     _description = 'helpdesk_mgmt_partner_security.helpdesk_mgmt_partner_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class res_partner(models.Model):
    _inherit = ['res.partner']
    helpdesk_partner = fields.Boolean('Client', help="Check this box if this contact is a helpdesk client only.")
    helpdesk_user_ids = fields.Many2many('res.users', string="Helpdesk User Access",
        compute='_compute_helpdesk_user_ids', search="_search_helpdesk_user_ids"
    )
    @api.depends('helpdesk_partner', )
    def _compute_helpdesk_user_ids(self):
        self.helpdesk_user_ids = False
        for partner in self:
            tickets = self.env['helpdesk.ticket'].search( [("partner_id", "=", partner.id)])
            for ticket in tickets:
                partner.helpdesk_user_ids |= ticket.user_ids
            # partnerlines = self.env['project_partner.partnerline'].search([("partner_id", "=", partner.id)])
            # for partnerline in partnerlines:
                # partner.helpdesk_partner_team_ids |= partnerline.ticket_id.team_id
    @api.model
    def _search_helpdesk_user_ids(self, operator, operand):
        assert operator != "not in", "Do not search message_follower_ids with 'not in'"
        tickets = self.env['helpdesk.ticket'].sudo().search([
            ('user_ids', operator, operand)])
        return [('id', 'in', [ticket.partner_id.id for ticket in tickets])]