# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_vendor = fields.Many2one(default_model='res.partner', related='company_id.default_vendor',
                                     string="Default Vendor", readonly=False)
