from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class HotelBooking(models.Model):
    _name = "hotel.booking"
    _description = "Hotel Booking"

    code = fields.Char()
    check_in = fields.Date(default=fields.Date.context_today)
    check_out = fields.Date()
    duration = fields.Integer(
        string="Số đêm",
        compute="_compute_duration_and_amount",
        store=True,
    )
    total_amount = fields.Integer(
        string="Tổng tiền",
        compute="_compute_duration_and_amount",
        store=True,
    )
    state = fields.Selection(
        [
            ("draft", "Nháp"),
            ("confirmed", "Đã xác nhận"),
            ("done", "Hoàn thành"),
        ],
        default="draft",
    )

    customer_id = fields.Many2one(
        "hotel.customer", string="Khách hàng", required=True
    )
    room_id = fields.Many2one(
        "hotel.room", string="Phòng", required=True
    )
    service_ids = fields.Many2many(
        "hotel.service", string="Dịch vụ thêm"
    )

    @api.depends("check_in", "check_out", "room_id", "service_ids")
    def _compute_duration_and_amount(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.duration = max(delta.days, 0)
            else:
                rec.duration = 0

            room_total = (rec.room_id.price_per_night or 0) * rec.duration

            service_total = sum(rec.service_ids.mapped("price"))

            rec.total_amount = room_total + service_total

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(
                    "Chỉ có thể xác nhận từ trạng thái Nháp!")
            rec.state = "confirmed"

    def action_done(self):
        for rec in self:
            if rec.state != "confirmed":
                raise ValidationError(
                    "Chỉ có thể hoàn thành từ trạng thái Đã xác nhận!")
            rec.state = "done"

    @api.onchange("room_id")
    def _onchange_room_id_warning(self):
        if self.room_id and self.room_id.status == "maintenance":
            return {
                "warning": {
                    "title": "Cảnh báo",
                    "message": "Phòng này đang bảo trì, vui lòng chọn phòng khác!",
                }
            }

    @api.onchange("check_in")
    def _onchange_check_in_set_checkout(self):
        if self.check_in:
            self.check_out = self.check_in + timedelta(days=1)

    @api.constrains("check_in", "check_out")
    def _check_dates(self):
        for rec in self:
            if rec.check_in and rec.check_out and rec.check_out <= rec.check_in:
                raise ValidationError("Ngày trả phòng không hợp lệ!")

    @api.constrains("room_id")
    def _check_room_not_occupied(self):
        for rec in self:
            if rec.room_id and rec.room_id.status == "occupied":
                raise ValidationError("Phòng này đang có khách ở!")
