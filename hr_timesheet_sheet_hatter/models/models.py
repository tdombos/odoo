# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeBase(models.Model):
    _inherit = ['hr.employee']
    department_ids = fields.Many2many('hr.department', string='Department', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    job_ids = fields.Many2many('hr.job', string='Job Position', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ref = fields.Char(related='address_home_id.ref')
    place_of_birth = fields.Char(related='address_home_id.place_of_birth')
    country_of_birth = fields.Many2one(related='address_home_id.country_of_birth')
    birthday = fields.Date(related='address_home_id.birthday')
    ssnid = fields.Char(related='address_home_id.ssnid')
    sinid = fields.Char(related='address_home_id.personaltaxnumber')
    identification_id = fields.Char(related='address_home_id.identification_id')
    passport_id = fields.Char(related='address_home_id.passport_id')
    country_id = fields.Many2one(related='address_home_id.nationality_id')
class Department(models.Model):
    _inherit = ['hr.department']
    member_ids = fields.Many2many('hr.employee', 'hr_department_hr_employee_rel', 'hr_department_id', 'hr_employee_id', string='Members', readonly=True)