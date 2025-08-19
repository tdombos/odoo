# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeBase(models.Model):
    _inherit = ['hr.employee']
    department_ids = fields.Many2many('hr.department', string='Department', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    job_ids = fields.Many2many('hr.job', string='Job Position', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    ref = fields.Char(related='work_contact_id.ref')
    place_of_birth = fields.Char(related='work_contact_id.place_of_birth')
    country_of_birth = fields.Many2one(related='work_contact_id.country_of_birth')
    birthday = fields.Date(related='work_contact_id.birthdate_date')
    ssnid = fields.Char(related='work_contact_id.ssnid')
    sinid = fields.Char(related='work_contact_id.personaltaxnumber')
    identification_id = fields.Char(related='work_contact_id.identification_id')
    passport_id = fields.Char(related='work_contact_id.passport_id')
    country_id = fields.Many2one(related='work_contact_id.nationality_id')
    gender = fields.Selection(related='work_contact_id.gender')

class Department(models.Model):
    _inherit = ['hr.department']
    member_ids = fields.Many2many('hr.employee', 'hr_department_hr_employee_rel', 'hr_department_id', 'hr_employee_id', string='Members', readonly=True)
