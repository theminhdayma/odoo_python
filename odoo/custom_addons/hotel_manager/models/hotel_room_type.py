from odoo import models, fields


class HotelRoomType(models.Model):
    _name = "hotel.room.type"
    _description = "Hotel Room Type"

    name = fields.Char(required=True)
    code = fields.Char()
