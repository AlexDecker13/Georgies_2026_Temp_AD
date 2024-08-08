# custom_sales_order/models/sale_order.py
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field_1 = fields.Char(string="Custom Field 1")
    custom_field_2 = fields.Boolean(string="Custom Field 2")
    custom_field_3 = fields.Date(string="Custom Field 3")
