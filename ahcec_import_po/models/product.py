# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    model_year = fields.Char('Model Year')
    grade = fields.Char('Grade (VC)')
    exterior_color = fields.Char('Exterior Color (VC)')
    interior_color = fields.Char('Interior Color (VC)')
    transmission_type = fields.Selection(
        [('automatic', 'AUTOMATIC'),
         ('cvt', 'CVT'),
         ('manual', 'MANUAL')],
        default='automatic', string="Transmission Type")
    vms_customer = fields.Char('VMS Customer')
    alj_suffix = fields.Char('ALJ Suffix (VC)')
    vehicle_model = fields.Char('Vehicle Model')
    brand = fields.Char('Brand')
    description = fields.Char('Description')
    complete_engine_number = fields.Char('Complete Engine Number')
    model_code = fields.Char('Model Code')
    action = fields.Char('Action')
    sales_document = fields.Char('Sales Document')
    request_delivery_date = fields.Date('Request Delivery Date')
    billing_document = fields.Char('Billing Document')
    bill_date = fields.Date('Bill Date')
    vehicle_wholesale_price = fields.Float('Vehicle Wholesale Price')
    broker_declaration_date = fields.Date('Broker Declaration Date')
    declaration_date = fields.Date('Declaration Date')
    netval = fields.Float('Net Val')
    vat_amount = fields.Float('VAT Amount')
    purchase_order = fields.Many2one('purchase.order','Purchase')

