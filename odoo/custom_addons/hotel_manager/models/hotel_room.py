from odoo import models, fields


class HotelRoom(models.Model):
    _name = "hotel.room"
    _description = "Hotel Room"

    name = fields.Char(required=True)
    floor = fields.Integer()
    price_per_night = fields.Integer()
    status = fields.Selection(
        [
            ("available", "Trống"),
            ("occupied", "Đang ở"),
            ("maintenance", "Bảo trì"),
        ],
        default="available",
    )
    type_id = fields.Many2one("hotel.room.type", string="Loại phòng")

    _sql_constraints = [
        ("room_name_unique",
         "UNIQUE(name)",
         "Tên phòng không được trùng!"),
        ("price_per_night_positive",
         "CHECK(price_per_night > 0)",
         "Giá phòng phải lớn hơn 0!"),
    ]
