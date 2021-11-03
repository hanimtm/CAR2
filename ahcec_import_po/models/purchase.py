# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_ids = fields.One2many('product.template', 'purchase_order', 'Products', required=True)