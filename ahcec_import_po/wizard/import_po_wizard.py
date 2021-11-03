# -*- coding: utf-8 -*-
# Part of AHCEC/VEICO.

import base64
import csv
from datetime import datetime

import xlrd
from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools import ustr


class ImportPoWizard(models.TransientModel):
    _name = 'import.po.wizard'

    import_type = fields.Selection([
        # ('csv', 'CSV File'),
        ('excel', 'Excel File')
    ], default="excel", string="Import File Type", required=True)
    file = fields.Binary(string="File", required=True)
    product_by = fields.Selection([
        ('name', 'Name'),
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode')
    ], default="name", string="Product By", required=True)
    is_create_vendor = fields.Boolean(string="Create Vendor?")
    is_confirm_order = fields.Boolean(string="Auto Confirm Order?")
    order_no_type = fields.Selection([
        ('auto', 'Auto'),
        # ('as_per_sheet', 'As per sheet')
    ], default="auto", string="Reference Number", required=True)

    def show_success_msg(self, counter, confirm_rec, skipped_line_no):

        action = self.env.ref('ahcec_import_po.ahcec_import_po_action').read()[0]
        action = {'type': 'ir.actions.act_window_close'}

        # open the new success message box
        view = self.env.ref('ahcec_import_po.ahcec_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        dic_msg = str(counter) + " Records imported successfully \n"
        dic_msg = dic_msg + str(confirm_rec) + " Records Confirm"
        if skipped_line_no:
            dic_msg = dic_msg + "\nNote:"
        for k, v in skipped_line_no.items():
            dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg

        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def import_po_apply(self):
        pol_obj = self.env['purchase.order.line']
        purchase_order_obj = self.env['purchase.order']
        if self and self.file:
            # For Excel
            if self.import_type == 'excel':
                counter = 1
                skipped_line_no = {}
                try:
                    wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
                    sheet = wb.sheet_by_index(0)
                    skip_header = True
                    running_po = None
                    created_po = False
                    created_po_list_for_confirm = []
                    created_po_list = []
                    partner = self.env.company.default_vendor
                    po_vals = {}
                    if not partner:
                        raise ValueError("Please add the Default Vendor in Settings")

                    po_vals.update({'partner_id': partner.id})
                    po_vals.update({'date_order': datetime.now()})
                    po_vals.update({'date_planned': datetime.now()})
                    created_po = purchase_order_obj.sudo().create(po_vals)
                    created_po_list_for_confirm.append(created_po.id)
                    created_po_list.append(created_po.id)

                    for row in range(sheet.nrows):
                        try:

                            if skip_header:
                                skip_header = False
                                counter = counter + 1
                                continue

                            if created_po:
                                vals = {}

                                type = False
                                if sheet.cell(row, 6).value == 'AUTOMATIC':
                                    type = 'automatic'
                                elif sheet.cell(row, 6).value == 'CVT':
                                    type = 'cvt'
                                else:
                                    type = 'manual'

                                search_product = self.env['product.product'].sudo().create({
                                    'name': sheet.cell(row, 1).value,
                                    'type': 'product',
                                    'company_id': False,
                                    'model_year': sheet.cell(row, 0).value,
                                    'grade': sheet.cell(row, 2).value,
                                    'default_code': sheet.cell(row, 3).value,
                                    'exterior_color': sheet.cell(row, 4).value,
                                    'interior_color': sheet.cell(row, 5).value,
                                    'transmission_type': type,
                                    'vms_customer': sheet.cell(row, 7).value,
                                    'alj_suffix': sheet.cell(row, 8).value,
                                    'vehicle_model': sheet.cell(row, 9).value,
                                    'purchase_order': created_po.id
                                })
                                if search_product:
                                    vals.update({'product_id': search_product.id})
                                    vals.update({'name': search_product.name})
                                    vals.update({'product_qty': 1})
                                    vals.update({'product_uom': search_product.uom_po_id.id})
                                    vals.update({'price_unit': search_product.standard_price})
                                    vals.update({'date_planned': datetime.now()})
                                    vals.update({'order_id': created_po.id})
                                    created_pol = pol_obj.create(vals)
                                    counter = counter + 1
                            else:
                                skipped_line_no[str(counter)] = " - Purchase Order not created. "
                                counter = counter + 1
                                continue

                        except Exception as e:
                            skipped_line_no[str(counter)] = " - Value is not valid " + ustr(e)
                            counter = counter + 1
                            continue
                    if created_po_list_for_confirm and self.is_confirm_order is True:
                        purchase_orders = purchase_order_obj.search([('id', 'in', created_po_list_for_confirm)])
                        if purchase_orders:
                            for purchase_order in purchase_orders:
                                purchase_order.button_confirm()
                    else:
                        created_po_list_for_confirm = []

                except Exception as e:
                    raise UserError(_("Sorry, Your excel file does not match with our format " + ustr(e)))

                if counter > 1:
                    completed_records = len(created_po_list)
                    confirm_rec = len(created_po_list_for_confirm)
                    res = self.show_success_msg(completed_records, confirm_rec, skipped_line_no)
                    return res
