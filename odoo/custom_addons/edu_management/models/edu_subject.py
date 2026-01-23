
from odoo import models, fields, api


class EduSubject(models.Model):
    _name = 'edu.subject'
    _description = 'Môn học/Chuyên ngành'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Tên Môn/Chuyên ngành',
        required=True,
        tracking=True,
        help='VD: Lập trình, Ngoại ngữ, Kinh tế'
    )
    code = fields.Char(
        string='Mã',
        tracking=True,
        help='Mã định danh chuyên ngành'
    )
    description = fields.Text(
        string='Mô tả',
        tracking=True
    )
    category = fields.Selection([
        ('it', 'CNTT (IT)'),
        ('economics', 'Kinh tế'),
        ('language', 'Ngoại ngữ'),
        ('other', 'Khác'),
    ], string='Phân loại', default='other', required=True,
        tracking=True,
        help='Phân loại chuyên ngành: IT, Kinh tế, Ngoại ngữ')

    course_ids = fields.One2many(
        'edu.course',
        'subject_id',
        string='Các Khóa học',
        help='Danh sách các khóa học thuộc chuyên ngành này'
    )
    course_count = fields.Integer(
        string='Số lượng Khóa học',
        compute='_compute_course_count',
        store=True
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Mã chuyên ngành phải duy nhất!')
    ]

    @api.depends('course_ids')
    def _compute_course_count(self):
        for record in self:
            record.course_count = len(record.course_ids)
