from odoo import api, fields, models


class School(models.Model):
    _name = 'school.management.school'
    _description = 'School'

    name = fields.Char(string='School Name', required=True)
    location = fields.Char(string='Location')
    start_date = fields.Date(string='Start Date')
    student_ids = fields.One2many(
        comodel_name='school.management.student',
        inverse_name='school_id',
        string='Students',
    )
    exam_ids = fields.One2many(
        comodel_name='school.management.exam',
        inverse_name='school_id',
        string='Exams',
    )

    @api.model
    def add_school(self, vals):
        """Thêm mới trường học."""
        return self.create(vals)

    def update_school(self, vals):
        """Cập nhật thông tin trường học."""
        self.write(vals)
        return True

