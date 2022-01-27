# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import xlrd
from xlrd import open_workbook
import base64
import os
from odoo.exceptions import UserError, ValidationError
import csv
#from cStringIO import StringIO
from io import StringIO
from io import BytesIO
#import urlparse
import urllib.parse as urlparse
import requests
import codecs


class importwizard(models.TransientModel):
    _name = 'import.attachment'
    _description = 'import.attachment.wizard'

    file = fields.Binary('File')
    file_fname = fields.Char(string='File name')

    def file_type(self):
        if self.file:
            filename,filetype = os.path.splitext(self.file_fname)
            return filetype


    @api.onchange('file')
    @api.depends('file','file_fname')
    def check_file_type(self):
        filetype=self.file_type()
        values = {}
        if filetype and filetype.lower() not in ['.xls','.xlsx','.csv']:
            values = {'warning':{'title':'Error!!','message':'Invalid file type!!!\n Choose excel or csv file format.'},
                            'value':{
                                    'file':None,
                                    'file_fname':None
                                    }
                    }
        return values

    def is_absolute(self,url):
        return bool(urlparse.urlparse(url).netloc)


    def write_file(self,data):
        print('data',data)
        for row in data:
            print('row',row)
            if self.is_absolute(row.get('file')):
                img_b64 = base64.b64encode(requests.get(row.get('file')).content)
            else:
                with open(row.get('file'),'rb') as f:
                    # import base64
                    img_b64 = base64.b64encode(f.read())
                    # img_b64 = f.read().encode('base64')
            res_id = self.env['ir.model.data'].get_object_reference(row.get('module'),row.get('id'))
            if img_b64:
                attachment = {'name': row.get('name'),    
                    'datas': img_b64, 
                    'datas_fname': row.get('filename'), 
                    'res_model': row.get('res_model'), 
                    'res_id': res_id[1]}
                self.env['ir.attachment'].create(attachment) 
            else:
                raise UserError(_("Error!!!\nInvalid file path for '%s'")%(row.get('id')))

    def get_file(self):
        if self.file:
            filetype = self.file_type()
            file_file  = base64.decodestring(self.file)

            # print('file_file',type(file_file))
            if filetype in ['.xlsx','.xls']:
                xl_data = self.get_xlData(file_file)
                self.write_file(xl_data)
            elif filetype in ['.csv']:
                csv_data = self.get_csvData(file_file)
                # csv_data = self.get_csvData(self.file)
                self.write_file(csv_data)
        else:
            raise UserError(_('Choose a file first!!!'))

    def get_xlData(self,data):
        book = xlrd.open_workbook(file_contents=data)
        sheet = book.sheet_by_index(0)
        first_row = [] # The row where we stock the name of the column
        for col in range(sheet.ncols):
            first_row.append( sheet.cell_value(0,col) )
            # transform the workbook to a list of dictionaries
        data =[]
        for row in range(1, sheet.nrows):
                elm = {}
                for col in range(sheet.ncols):
                    elm[first_row[col]]=sheet.cell_value(row,col)
                data.append(elm)
        return data

    def get_csvData(self,data):
        csv_data = str(data,'utf-8')
        encoding = 'utf-8'
        csv_iteratorDict = csv.DictReader(StringIO(csv_data))

        return csv_iteratorDict

class importwizard2(models.TransientModel):
    _name = 'import.ticketdocument'
    _description = 'import.ticketdocument.wizard'

    file = fields.Binary('File')
    file_fname = fields.Char(string='File name')

    def file_type(self):
        if self.file:
            filename,filetype = os.path.splitext(self.file_fname)
            return filetype


    @api.onchange('file')
    @api.depends('file','file_fname')
    def check_file_type(self):
        filetype=self.file_type()
        values = {}
        if filetype and filetype.lower() not in ['.xls','.xlsx','.csv']:
            values = {'warning':{'title':'Error!!','message':'Invalid file type!!!\n Choose excel or csv file format.'},
                            'value':{
                                    'file':None,
                                    'file_fname':None
                                    }
                    }
        return values

    def is_absolute(self,url):
        return bool(urlparse.urlparse(url).netloc)


    def write_file(self,data):
        print('data',data)
        for row in data:
            print('row',row)
            if self.is_absolute(row.get('file')):
                img_b64 = base64.b64encode(requests.get(row.get('file')).content)
            else:
                with open(row.get('file'),'rb') as f:
                    # import base64
                    img_b64 = base64.b64encode(f.read())
                    # img_b64 = f.read().encode('base64')
            res_id = self.env['ir.model.data'].get_object_reference(row.get('module'),row.get('id'))
            if img_b64:
                attachment = {'name': row.get('name'),    
                    'datas': img_b64, 
                    'datas_fname': row.get('filename'), 
                    'res_model': row.get('res_model'), 
                    'res_id': res_id[1]}
                self.env['ir.attachment'].create(attachment) 
            else:
                raise UserError(_("Error!!!\nInvalid file path for '%s'")%(row.get('id')))

    def get_file(self):
        if self.file:
            filetype = self.file_type()
            file_file  = base64.decodestring(self.file)

            # print('file_file',type(file_file))
            if filetype in ['.xlsx','.xls']:
                xl_data = self.get_xlData(file_file)
                self.write_file(xl_data)
            elif filetype in ['.csv']:
                csv_data = self.get_csvData(file_file)
                # csv_data = self.get_csvData(self.file)
                self.write_file(csv_data)
        else:
            raise UserError(_('Choose a file first!!!'))

    def get_xlData(self,data):
        book = xlrd.open_workbook(file_contents=data)
        sheet = book.sheet_by_index(0)
        first_row = [] # The row where we stock the name of the column
        for col in range(sheet.ncols):
            first_row.append( sheet.cell_value(0,col) )
            # transform the workbook to a list of dictionaries
        data =[]
        for row in range(1, sheet.nrows):
                elm = {}
                for col in range(sheet.ncols):
                    elm[first_row[col]]=sheet.cell_value(row,col)
                data.append(elm)
        return data

    def get_csvData(self,data):
        csv_data = str(data,'utf-8')
        encoding = 'utf-8'
        csv_iteratorDict = csv.DictReader(StringIO(csv_data))

        return csv_iteratorDict