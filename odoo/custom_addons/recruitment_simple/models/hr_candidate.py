from odoo import models, fields

class HrCandidate(models.Model):
    _name = 'hr.candidate'
    _description = 'Candidate Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Tích hợp Chatter (tin nhắn, note)
    _rec_name = 'name'

    name = fields.Char(string='Tên ứng viên', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string='Giới tính', tracking=True)
    
    # Status Pipeline (Quy trình tuyển dụng)
    status = fields.Selection([
        ('new', 'Mới ứng tuyển'),
        ('test', 'Đang làm bài test'),
        ('interview', 'Phỏng vấn'),
        ('offer', 'Đề nghị lương'),
        ('done', 'Đã tuyển'),
        ('cancel', 'Từ chối')
    ], string='Trạng thái', default='new', tracking=True, group_expand='_expand_states')

    birthday = fields.Date(string='Ngày sinh')
    # Fixing persistent view cache error by keeping aliases
    birth_date = fields.Date(related='birthday', string='Ngày sinh (Fix)', store=True)
    
    cv_content = fields.Text(string='Nội dung CV tóm tắt')
    expected_salary = fields.Integer(string='Lương mong muốn', tracking=True)
    # Fixing persistent view cache error by keeping aliases
    desired_salary = fields.Integer(related='expected_salary', string='Lương mong muốn (Fix)', store=True)
    
    # Re-enable this field because old views/filters still reference it
    is_hired = fields.Boolean(string='Đã tuyển chưa?', default=False)

    manager_note = fields.Text(
        string='Đánh giá của Sếp',
        groups='recruitment_simple.group_hr_manager'
    )

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).status.selection]

    def action_do_something(self):
        print("Button clicked!")
        return True
