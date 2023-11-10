# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class GrantCall(models.Model):
    _inherit = "grant.call"

    enable_evaluation = fields.Boolean('Enable Evaluation', compute='_check_for_evaluation')
    eval_template_id = fields.Many2one('grant.proposal.evaluation.template', string="Proposal Evaluation Template", ondelete="restrict", 
                                help="""Choose the evaluation template that you would like to use for this call. 
                                        You can edit questions on individual evaluation records if needed.""")
    evaluation_guidelines = fields.Text('Evaluation Guidelines', help="Guidelines noted here will also be listed on each proposal evaluation record.")
    selected_proposal_ids = fields.Many2many('grant.proposal', string="Selected Proposals", 
                                help="Confirmed proposals will automatically be added to this list. However, you can still add proposals manually if required.")
    selection_justification = fields.Text('Justification/Notes', help="Any remarks relevant to the proposal selection and evaluation process.")

    def get_checklist_summary_titles(self):
        """Function used in the 'Proposal Checklist Summary' report to print the first row of the checklist table"""
        evaluation_records = self.env['grant.proposal.evaluation'].search([('call_id', '=', self.id),('state', 'in', ['done','to_approve','draft'])])
        return sorted(list(set(evaluation_records.mapped('checklist_item_ids.name'))))

    def get_checklist_summary_lines(self):
        """Function used in the 'Proposal Checklist Summary' report to print the checklist status for each of the proposals of a call"""
        evaluation_records = self.env['oroposal.evaluation'].search([('call_id', '=', self.id),('state', '=', ['done','to_approve', 'draft'])])
        checklist_item_names = sorted(list(set(evaluation_records.mapped('checklist_item_ids.name'))))
        
        checklist_l = []
        for rec in evaluation_records:
            applicant_list = []
            applicant_list.append(rec.applicant_id.name)
            applicant_list.append(rec.grant_proposal_id.name)
            partner_dict = {}
            if len(rec.checklist_item_ids) == 0:
                for name in checklist_item_names:
                    partner_dict[name] = 'N/A' 
            else:
                for checklist_title in checklist_item_names:
                    for line in rec.checklist_item_ids:
                        if line.name == checklist_title:
                            partner_dict[line.name] = line.item_clear
            for title in checklist_item_names:
                if title not in partner_dict:
                    partner_dict[title] = 'N/A'

            # sorted_partner_dict = {}
            sorted_partner_dict = {key: value for key, value in sorted(partner_dict.items())}

            applicant_list.append(sorted_partner_dict)
            checklist_l.append(applicant_list)
        return checklist_l

    def get_evaluation_questions(self):
        """Function used in the Evaluation Summary report to generate the first row for the evaluation scoring table."""
        evaluation_records = self.env['grant.proposal.evaluation'].search([('call_id', '=', self.id),('state', 'in', ['done','to_approve', 'draft'])])
        question_titles = sorted(list(set(evaluation_records.mapped('question_ids.name'))))
        question_titles.append('Average Score')
        return question_titles

    def get_evaluation_summary_lines(self):
        """Function used in the Evaluation Summary report to generate the data for the evaluation scoring table."""
        evaluation_records = self.env['prpposal.evaluation'].search([('call_id', '=', self.id),('state', 'in', ['done','to_approve', 'draft'])])
        question_titles = sorted(list(set(evaluation_records.mapped('question_ids.name'))))
        
        eval_list = []
        for rec in evaluation_records:
            applicant_list = []
            applicant_list.append(rec.applicant_id.name)
            applicant_list.append(rec.grant_call_id.name)
            partner_dict = {}
            if len(rec.question_ids) == 0:
                for name in question_titles:
                    partner_dict[name] = ' - '
            else:
                for question in question_titles:
                    for line in rec.question_ids:
                        if line.name == question:
                            partner_dict[line.name] = line.score
            for title in question_titles:
                if title not in partner_dict:
                    partner_dict[title] = ' - '

            # sorted_partner_dict = {}
            sorted_partner_dict = {key: value for key, value in sorted(partner_dict.items())}
            sorted_partner_dict['Average Score'] = round(rec.score_avg,2)
            applicant_list.append(sorted_partner_dict)
            eval_list.append(applicant_list)

        return eval_list

