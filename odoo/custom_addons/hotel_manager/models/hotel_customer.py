from odoo import models, fields


class HotelCustomer(models.Model):
    _name = "hotel.customer"
    _description = "Hotel Customer"
    _order = "name"

    name = fields.Char(required=True)
    identity_card = fields.Char()
    phone = fields.Char()

    _sql_constraints = [
        ("identity_card_unique",
         "UNIQUE(identity_card)",
         "Số CMND/CCCD đã tồn tại!"),
    ]

    booking_ids = fields.One2many(
        "hotel.booking", "customer_id", string="Lịch sử đặt phòng"
    )
