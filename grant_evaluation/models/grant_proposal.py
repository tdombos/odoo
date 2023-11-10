# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError

class GrantProposal(models.Model):
    _inherit = "grant.proposal"

    show_eval_button = fields.Boolean(string='Allow Eval Creation', default=False, copy=False, compute="_compute_show_evaluation_button")
    has_evaluation = fields.Boolean(string='Has Evaluation', default=False, copy=False)
    evaluation_count = fields.Integer(compute="_compute_evaluations_count")

    def get_checklist_item_ids(self):
        checklist_list = []
        for item in self.call_id.eval_template_id.checklist_item_ids:
            checklist_list.append((0, 0, {'name': item.name, 'item_clear': 'no'}))
        return checklist_list

    def get_question_ids(self):
        questions_list = []
        for question in self.call_id.eval_template_id.question_ids:
            questions_list.append((0, 0, {'name': question.name}))
        return questions_list
    
    def get_bid_evaluation_record(self):
        self.ensure_one()
        proposal_evaluation_record = self.env['grant.proposal.evaluation'].search([('proposal_id', '=', self.id)])
        if proposal_evaluation_record:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Proposal Evaluation',
                'view_mode': 'form',
                'res_model': 'grant.proposal.evaluation',
                'res_id': proposal_evaluation_record.id,
                'domain': [('proposal_id', '=', self.id)],
            }
    
    def create_bid_evaluation(self):
        if not self.call_id.eval_template_id:
            raise UserError(_("You have not specified a proposal evaluation template on the call record. Please set the evaluation template and retry."))
        
        proposal_evaluation_record = self.env['grant.proposal.evaluation'].sudo().create({
            'name': f'Proposal Evaluation - {self.call_id.name} - {self.applicant_id.name}',
            'proposal_id': self.id,
            'call_id': self.call_id.id,
            'applicant_id': self.applicant_id.id,
            # user_id equals to current logged in user:
            'user_id': self.env.user.id,
            'date': fields.Date.today(),
            'evaluation_guidelines': self.call_id.evaluation_guidelines,
            'score_limit': self.call_id.eval_template_id.score_limit,
            'checklist_item_ids': self.get_checklist_item_ids(),
            'question_ids': self.get_question_ids()
          })
  
        self.write({'has_evaluation': True})
        return self.get_proposal_evaluation_record()

    # update the selected proposal field once an rfq is confirmed in an agreement
    def button_confirm(self):
        res = super(GrantProposal, self).button_confirm()
        for po in self:
            if not po.call_id:
                continue
            po.call_id.selected_proposal_ids = [(4, po.id)]
        return res
    
    def _compute_evaluations_count(self):
        ProposalEvaluations = self.env['grant.proposal.evaluation']
        self.evaluation_count = ProposalEvaluations.search_count([('proposal_id', '=', self.id)])

    def _compute_show_evaluation_button(self):
        if not self.call_id or self.has_evaluation:
            self.show_eval_button = False
        else:
            self.show_eval_button = True
