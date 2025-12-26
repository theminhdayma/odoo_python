# -*- coding: utf-8 -*-

from odoo import models, fields, api

# 1. MODEL MÔN HỌC
class TrainingSubject(models.Model):
    _name = 'training.subject'
    _description = 'Môn học'

    name = fields.Char(string="Tên môn", required=True)
    code = fields.Char(string="Mã môn")
    description = fields.Text(string="Mô tả đề cương")

# 2. MODEL GIẢNG VIÊN
class TrainingTeacher(models.Model):
    _name = 'training.teacher'
    _description = 'Giảng viên'

    name = fields.Char(string="Tên giảng viên", required=True)
    phone = fields.Char(string="Số điện thoại")
    skills = fields.Text(string="Kỹ năng")

# 3. MODEL SINH VIÊN
class TrainingStudent(models.Model):
    _name = 'training.student'
    _description = 'Sinh viên'

    name = fields.Char(string="Tên sinh viên", required=True)
    email = fields.Char(string="Email")
    student_id = fields.Char(string="Mã sinh viên")

# 4. MODEL LỚP HỌC
class TrainingClass(models.Model):
    _name = 'training.class'
    _description = 'Lớp học'

    name = fields.Char(string="Tên lớp", required=True)
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")

    description = fields.Char(string="Mô tả lớp học")
    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('open', 'Đang mở'),
        ('closed', 'Đã đóng')
    ], string="Trạng thái", default='draft')
    price_per_student = fields.Integer(string="Học phí/sinh viên", default=1000000)
    total_revenue = fields.Integer(string="Tổng doanh thu", compute='_compute_total_revenue', store=True)

    # Relationships
    subject_id = fields.Many2one('training.subject', string="Môn học", required=True)
    teacher_id = fields.Many2one('training.teacher', string="Giảng viên")
    student_ids = fields.Many2many('training.student', string="Danh sách sinh viên")
    session_ids = fields.One2many('training.session', 'class_id', string="Lịch học chi tiết")

    @api.depends('student_ids', 'price_per_student')
    def _compute_total_revenue(self):
        for record in self:
            record.total_revenue = len(record.student_ids) * record.price_per_student

    @api.onchange('name', 'start_date')
    def _onchange_description(self):
        for record in self:
            if record.name and record.start_date:
                record.description = f"Lớp {record.name} bắt đầu từ {record.start_date}"
            else:
                record.description = "Mô tả lớp học"
    
    @api.onchange('price_per_student')
    def _onchange_price_warning(self):
        self.ensure_one()
        if self.price_per_student and self.price_per_student < 500000:
            return {
                'warning': {
                    'title': "Cảnh báo học phí thấp",
                    'message': "Học phí/sinh viên thấp hơn mức tối thiểu 500,000 VND."
                }
            }
            
    @api.constrains('end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date and record.end_date < record.start_date:
                raise models.ValidationError("Ngày kết thúc phải sau ngày bắt đầu.")
    
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing_class = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing_class:
                raise models.ValidationError("Tên lớp học phải là duy nhất.")
            elif not record.name:
                raise models.ValidationError("Tên lớp học không được để trống.")
# 5. MODEL BUỔI HỌC (SESSION)
class TrainingSession(models.Model):
    _name = 'training.session'
    _description = 'Buổi học'

    name = fields.Char(string="Nội dung buổi học", required=True)
    date = fields.Date(string="Ngày học", default=fields.Date.today)
    duration = fields.Integer(string="Thời lượng (phút)")
    
    # Many2one ngược về Lớp học
    class_id = fields.Many2one('training.class', string="Lớp học")