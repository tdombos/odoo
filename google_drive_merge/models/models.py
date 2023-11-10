# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError
import requests
from odoo.addons.google_account.models.google_service import GOOGLE_TOKEN_ENDPOINT, TIMEOUT
import re
import json
from odoo.tools import safe_eval

class GoogleDrive(models.Model):
    _inherit = 'google.drive.config'
    def copy_doc(self, res_id, template_id, name_gdocs, res_model):
        res = super(GoogleDrive, self).copy_doc(res_id, template_id, name_gdocs, res_model)
        file_id = self._get_key_from_url(res['url'])
        access_token = self.get_access_token(scope='https://www.googleapis.com/auth/documents')
        request_url = "https://docs.googleapis.com/v1/documents/%s?access_token=%s" % (file_id, access_token)
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        req = requests.get(request_url, headers=headers, timeout=TIMEOUT)
        req.raise_for_status()
        content = req.content.decode("utf-8") 
        mergefields = re.findall("\${(.*)}", content)
        changes=[]
        record = self.env[res_model].browse(res_id)
        variables = {}
        variables['object'] = record
        for field in mergefields:
            change = {
                'replaceAllText': {
                    'containsText': {
                        'text': '${'+field+'}',
                        'matchCase':  'true'
                    },
                    'replaceText': safe_eval.safe_eval(field, variables),
                }
            }
            changes.append(change)
        changes_json = json.dumps({'requests': changes})
        request_url = "https://docs.googleapis.com/v1/documents/%s:batchUpdate?access_token=%s" % (file_id, access_token)
        req2 = requests.post(request_url, data=changes_json, headers={'content-type': 'application/json', 'If-Match': '*'}, timeout=TIMEOUT)
        req2.raise_for_status()
        return res