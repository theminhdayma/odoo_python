from odoo import api, fields, models


class Student(models.Model):
    _name = 'school.management.student'
    _description = 'Student'

    name = fields.Char(string='Student Name', required=True)
    age = fields.Integer(string='Age')
    school_id = fields.Many2one(
        comodel_name='school.management.school',
        string='School',
        ondelete='set null',
    )
    score = fields.Float(string='Score')

    @api.model
    def add_student(self, vals):
        """Thêm mới học viên và gán trường học."""
        return self.create(vals)

    def update_student(self, vals):
        """Cập nhật thông tin học viên."""
        self.write(vals)
        return True

