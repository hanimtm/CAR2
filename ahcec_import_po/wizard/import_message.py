# -*- coding: utf-8 -*-

from odoo import fields, models


class ImportMessage(models.TransientModel):
    _name = 'import.message.wizard'

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    name = fields.Text(string="Message", readonly=True, default=get_default)
