
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(
        string='Là Giảng viên',
        default=False,
        tracking=True,
        help='Đánh dấu nếu partner này là giảng viên'
    )
    session_teaching_ids = fields.One2many(
        'edu.session',
        'instructor_id',
        string='Lớp đang dạy',
        help='Danh sách các lớp học mà giảng viên này đang dạy'
    )
    session_teaching_count = fields.Integer(
        string='Số lớp đang dạy',
        compute='_compute_session_teaching_count',
        store=True
    )
    session_attending_ids = fields.Many2many(
        'edu.session',
        'edu_session_attendee_rel',
        'partner_id',
        'session_id',
        string='Lớp đang học',
        help='Danh sách các lớp mà học viên này đang tham gia'
    )

    @api.depends('session_teaching_ids')
    def _compute_session_teaching_count(self):
        for record in self:
            count = len(record.session_teaching_ids)
            record.session_teaching_count = count
