# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ProposalEvaluationTemplate(models.Model):
    _name = 'grant.proposal.evaluation.template'
    _description = 'Proposal Evaluation Template'

    name = fields.Char(string="Evaluation Template Name", required=True)
    evaluation_approach = fields.Boolean('Evaluation Approach')
    # scorable = fields.Boolean('Scorable?')
    score_limit = fields.Integer('Maximum Score', default=5)
    checklist_item_ids = fields.One2many('grant.proposal.template.checklist', 'evaluation_template_id',string="Proposal Checklist")
    question_ids = fields.One2many('grant.proposal.template.question', 'evaluation_template_id',string="Proposal Evaluation Questions")


class ProposalTemplateQuestion(models.Model):
    _name = 'grant.proposal.template.question'
    _description = 'Proposal Template Question'

    name = fields.Char(string="Question/Factor", required=True)
    evaluation_template_id = fields.Many2one('grant.proposal.evaluation.template')

    
class ProposalTemplateChecklist(models.Model):
    _name = 'grant.proposal.template.checklist'
    _description = 'Proposal Template Checklist'

    name = fields.Char(string="Item", required=True)
    evaluation_template_id = fields.Many2one('grant.proposal.evaluation.template')