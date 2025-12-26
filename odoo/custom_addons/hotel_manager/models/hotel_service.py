from odoo import models, fields


class HotelService(models.Model):
    _name = "hotel.service"
    _description = "Hotel Service"

    name = fields.Char(required=True)
    price = fields.Integer()

    _sql_constraints = [
        ("price_positive",
         "CHECK(price > 0)",
         "Giá dịch vụ phải lớn hơn 0!"),
    ]
