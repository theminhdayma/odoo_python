from odoo import api, fields, models


class Exam(models.Model):
    _name = 'school.management.exam'
    _description = 'Exam'

    exam_date = fields.Date(string='Exam Date')
    subject = fields.Char(string='Subject')
    school_id = fields.Many2one(
        comodel_name='school.management.school',
        string='School',
        ondelete='set null',
    )
    student_ids = fields.Many2many(
        comodel_name='school.management.student',
        relation='school_exam_student_rel',
        column1='exam_id',
        column2='student_id',
        string='Students',
    )

    def compute_average_score(self):
        """Tính điểm trung bình học viên trong kỳ thi."""
        for exam in self:
            scores = exam.student_ids.mapped('score')
            valid_scores = [s for s in scores if s is not None]
            exam.avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0.0

    avg_score = fields.Float(string='Average Score', compute='compute_average_score', store=False)

