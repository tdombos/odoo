# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hr_partner_security(models.Model):
#     _name = 'hr_partner_security.hr_partner_security'
#     _description = 'hr_partner_security.hr_partner_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class res_partner(models.Model):
    _inherit = ['res.partner']
    employee = fields.Boolean(help="Is true if contact is an Employee.", compute='_compute_employee', store=True)
    department_user_ids = fields.Many2many('res.users', string="Shared Department Members",
        compute='_compute_department_user_ids', search='_search_department_user_ids')
    
    @api.depends('employee_ids')
    def _compute_employee(self):
        for partner in self:
            if partner.employees_count>0: 
                partner.employee = True
            else: 
                partner.employee = False
    @api.depends('employee_ids')
    def _compute_department_user_ids(self):
        self.department_user_ids = False
        for partner in self.sudo():
#           raise UserError(partner.employee_ids.department_ids.member_ids.user_id)
            partner.department_user_ids = partner.employee_ids.department_ids.member_ids.user_id
    def _search_department_user_ids(self, operator, operand):
        departments = self.env['hr.department'].sudo().search([
            ('member_ids.user_id', operator, operand)])
        partners = departments.member_ids.address_home_id
#        raise UserError(partners)
        return [('id', 'in', [partner.id for partner in partners])]
class HrEmployeeBase(models.Model):
    _inherit = ['hr.employee']
    department_user_ids = fields.Many2many('res.users', string="Shared Department Members",
        compute='_compute_department_user_ids', search='_search_department_user_ids')
    def _compute_department_user_ids(self):
        self.department_user_ids = False
        for employee in self.sudo():
            employee.department_user_ids = employee.department_ids.member_ids.user_id
    def _search_department_user_ids(self, operator, operand):
        departments = self.env['hr.department'].sudo().search([
            ('member_ids.user_id', operator, operand)])
        employees = departments.member_ids
#        raise UserError(partners)
        return [('id', 'in', [employee.id for employee in employees])]
