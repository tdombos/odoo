# -*- coding: utf-8 -*-
################################################################################# 
#
#    Author: Abdullah Khalil. Copyrights (C) 2022-TODAY reserved. 
#    Email: abdulah.khaleel@gmail.com
#    You may use this app as per the rules outlined in the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3. 
#    See <http://www.gnu.org/licenses/> for more detials.
#   
#
################################################################################# 

{
    'name': "Proposal Evaluation",   
    'summary': "Evaluate and score proposals",   
    'description': """
        This app allows you to evaluate grant proposals recieved as part of a 
        calls for proposals. It also provides the ablitity to
        create and use multiple evaluation templates, and setup each template
        with its own set of guidelines, checklists and evaluation/scoring criteria.
    """,   
    'author': "Tamás Dombos and Abdullah Khalil",
    'website': "https://github.com/abdulah-khaleel",
    'category': 'Grant',
    'version': '15.0.0.0',
     "license": "LGPL-3",
    'depends': ['grant'],
    # 'data': [
        # 'security/ir.model.access.csv',
        # 'views/proposal_evaluation_template.xml',
        # 'views/grant_call.xml',
        # 'views/grant_proposal.xml',
        # 'views/proposal_evaluation.xml',
        # 'views/res_config_settings_views.xml',
        # 'reports/proposal_evaluation_sheet.xml',
        # 'reports/proposals_checklist_summary.xml',
        # 'reports/proposals_evaluation_summary.xml',
        # 'reports/proposals_comparative_report.xml',
    # ],
    'images': ["static/description/banner-v15.png"],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
} 
