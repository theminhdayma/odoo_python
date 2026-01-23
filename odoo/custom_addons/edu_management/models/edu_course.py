# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EduCourse(models.Model):
    _name = 'edu.course'
    _description = 'Khóa học (Course)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Tên Khóa học',
        required=True,
        tracking=True,
        help='Tên khóa học phải duy nhất, không trùng lặp'
    )
    description = fields.Html(
        string='Mô tả',
        tracking=True,
        help='Mô tả chi tiết về khóa học'
    )
    active = fields.Boolean(
        string='Đang hoạt động',
        default=True,
        tracking=True,
        help='Bỏ tick để đóng khóa học'
    )
    responsible_id = fields.Many2one(
        'res.users',
        string='Người phụ trách',
        tracking=True,
        help='User phụ trách khóa học này'
    )
    subject_id = fields.Many2one(
        'edu.subject',
        string='Chuyên ngành/Môn học',
        tracking=True,
        help='Khóa học thuộc chuyên ngành nào'
    )
    session_ids = fields.One2many(
        'edu.session',
        'course_id',
        string='Danh sách Lớp học'
    )
    session_count = fields.Integer(
        string='Số Lớp học',
        compute='_compute_session_count',
        store=True
    )
    level = fields.Selection([
        ('basic', 'Cơ bản'),
        ('advanced', 'Nâng cao'),
    ], string='Trình độ', default='basic')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'Tên khóa học phải duy nhất! Không được trùng lặp.')
    ]

    @api.depends('session_ids')
    def _compute_session_count(self):
        for record in self:
            record.session_count = len(record.session_ids)

    @api.onchange('responsible_id')
    def _onchange_responsible_id(self):
        """
        Khi chọn User phụ trách -> Tự động điền email vào mô tả
        """
        if self.responsible_id and self.responsible_id.email:
            email_text = (
                f"<p><strong>Email người phụ trách:</strong> "
                f"{self.responsible_id.email}</p>"
            )
            if self.description:
                self.description = self.description + email_text
            else:
                self.description = email_text
