# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"      # Tên bảng trong DB sẽ là estate_property
    _description = "Hồ sơ Bất động sản"

    # --- CÁC TRƯỜNG CƠ BẢN ---
    name = fields.Char(string='Tên tài sản', required=True)
    description = fields.Text(string='Mô tả')
    postcode = fields.Char(string='Mã bưu điện')
    date_availability = fields.Date(string='Ngày mở bán', copy=False, default=fields.Date.today())
    expected_price = fields.Float(string='Giá mong muốn', required=True)
    selling_price = fields.Float(string='Giá bán', readonly=True, copy=False)

    # --- CÁC TRƯỜNG CHI TIẾT ---
    bedrooms = fields.Integer(string='Số phòng ngủ', default=2)
    living_area = fields.Integer(string='Diện tích ở (m2)')
    facades = fields.Integer(string='Số mặt tiền')
    garage = fields.Boolean(string='Có Gara?')
    garden = fields.Boolean(string='Có vườn?')
    garden_area = fields.Integer(string='Diện tích vườn (m2)')

    # --- TRƯỜNG SELECTION ---
    garden_orientation = fields.Selection(
        string='Hướng vườn',
        selection=[
            ('north', 'Bắc'), ('south', 'Nam'), ('east', 'Đông'), ('west', 'Tây')
        ],
        help="Hướng của khu vườn chính"
    )