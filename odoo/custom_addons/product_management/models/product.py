from odoo import fields, models


class Product(models.Model):
    _name = 'product.management.product'
    _description = 'Product'

    product_name = fields.Char(string='Product Name', required=True)
    product_price = fields.Float(string='Price', default=0.0, required=True)
    product_quantity = fields.Integer(string='Quantity', default=0, required=True)

