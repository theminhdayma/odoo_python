
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class EduSession(models.Model):
    _name = 'edu.session'
    _description = 'Lớp học (Session)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(
        string='Tên Lớp học',
        required=True,
        tracking=True
    )
    code = fields.Char(
        string='Mã Lớp',
        readonly=True,
        copy=False
    )
    active = fields.Boolean(
        string='Đang hoạt động',
        default=True
    )
    classroom_id = fields.Many2one(
        'edu.classroom',
        string='Phòng học',
        tracking=True,
        help='Chọn phòng học cho lớp này'
    )
    course_id = fields.Many2one(
        'edu.course',
        string='Khóa học',
        required=True,
        tracking=True
    )
    instructor_id = fields.Many2one(
        'res.partner',
        string='Giảng viên',
        domain=[('is_instructor', '=', True)],
        tracking=True,
        help='Chỉ hiển thị Partner được đánh dấu là Giảng viên'
    )
    start_date = fields.Date(
        string='Ngày bắt đầu',
        default=fields.Date.today,
        tracking=True
    )
    duration = fields.Float(
        string='Thời lượng (giờ)',
        help='Số giờ học của lớp',
        tracking=True
    )
    end_date = fields.Date(
        string='Ngày kết thúc',
        compute='_compute_end_date',
        store=True
    )
    seats = fields.Integer(
        string='Số chỗ ngồi',
        default=10,
        tracking=True
    )
    attendee_ids = fields.Many2many(
        'res.partner',
        'edu_session_attendee_rel',
        'session_id',
        'partner_id',
        string='Học viên',
        tracking=True
    )
    attendee_count = fields.Integer(
        string='Số học viên',
        compute='_compute_attendee_count',
        store=True
    )
    taken_seats = fields.Float(
        string='% Chỗ ngồi đã đặt',
        compute='_compute_taken_seats',
        store=True
    )
    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('open', 'Mở đăng ký'),
        ('done', 'Kết thúc'),
        ('cancel', 'Hủy'),
    ], string='Trạng thái', default='draft', tracking=True)

    product_id = fields.Many2one(
        'product.template',
        string='Học phí',
        domain=[('is_edu_fee', '=', True)],
        help='Chọn sản phẩm học phí cho lớp này'
    )
    revenue = fields.Monetary(
        string='Doanh thu',
        compute='_compute_revenue',
        store=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for session in self:
            if session.start_date and session.duration:
                days = session.duration / 8
                session.end_date = session.start_date + timedelta(days=days)
            else:
                session.end_date = session.start_date

    @api.depends('attendee_ids')
    def _compute_attendee_count(self):
        for session in self:
            session.attendee_count = len(session.attendee_ids)

    @api.depends('seats', 'attendee_count')
    def _compute_taken_seats(self):
        for session in self:
            if session.seats > 0:
                session.taken_seats = (
                    session.attendee_count / session.seats) * 100
            else:
                session.taken_seats = 0.0

    @api.depends('attendee_count', 'product_id',
                 'product_id.list_price')
    def _compute_revenue(self):
        for session in self:
            if session.product_id:
                price = session.product_id.list_price
                session.revenue = session.attendee_count * price
            else:
                session.revenue = 0.0

    @api.onchange('course_id')
    def _onchange_course_id(self):
        """
        Khi chọn Khóa học -> Tự động điền Giảng viên
        (responsible_id) của khóa đó
        """
        if self.course_id and self.course_id.responsible_id:
            instructor = self.course_id.responsible_id.partner_id
            if instructor and instructor.is_instructor:
                self.instructor_id = instructor

    @api.onchange('seats')
    def _onchange_seats(self):
        """
        Validate: Nếu nhập Số ghế < 0 -> Show warning popup
        và reset về 0
        """
        if self.seats < 0:
            self.seats = 0
            return {
                'warning': {
                    'title': 'Lỗi giá trị',
                    'message': 'Số chỗ ngồi không được âm!'
                }
            }

    @api.onchange('seats', 'attendee_ids')
    def _onchange_seats_attendees(self):
        """
        Cảnh báo khi số học viên vượt quá số chỗ ngồi
        """
        if self.seats > 0 and len(self.attendee_ids) > self.seats:
            return {
                'warning': {
                    'title': 'Cảnh báo',
                    'message': (
                        f'Số học viên ({len(self.attendee_ids)}) '
                        f'vượt quá số chỗ ngồi ({self.seats})!'
                    )
                }
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        """
        Constraint: Giảng viên phụ trách không được có tên
        trong danh sách học viên
        """
        for session in self:
            if (session.instructor_id and
                    session.instructor_id in session.attendee_ids):
                raise ValidationError(
                    f'Giảng viên "{session.instructor_id.name}" '
                    'không được là học viên của lớp này!'
                )

    @api.constrains('duration', 'start_date')
    def _check_duration_and_start_date(self):
        """
        Constraint: Thời lượng phải > 0,
        Ngày bắt đầu không được để trống
        """
        for session in self:
            if not session.start_date:
                raise ValidationError(
                    'Ngày bắt đầu không được để trống!'
                )
            if session.duration and session.duration <= 0:
                raise ValidationError(
                    'Thời lượng khóa học phải lớn hơn 0!'
                )

    @api.constrains('classroom_id', 'start_date', 'end_date')
    def _check_classroom_overlapping(self):
        """
        Constraint: Một phòng không được tổ chức 2 lớp ở
        thời gian trùng nhau
        """
        for session in self:
            if (not session.classroom_id or
                    not session.start_date or
                    not session.end_date):
                continue
            overlapping = self.env['edu.session'].search([
                ('classroom_id', '=', session.classroom_id.id),
                ('id', '!=', session.id),
                ('state', '!=', 'cancel'),
                '|',
                ('start_date', '<=', session.end_date),
                ('end_date', '>=', session.start_date),
            ])
            if overlapping:
                overlap_names = ', '.join([s.name for s in overlapping])
                raise ValidationError(
                    f'Phòng "{session.classroom_id.name}" '
                    f'trùng lịch với lớp: {overlap_names}!'
                )

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = (self.env['ir.sequence'].next_by_code(
                'edu.session') or 'New')
        return super(EduSession, self).create(vals)

    @api.model
    def default_get(self, fields_list):
        """
        Khi tạo lớp mới, tự động điền start_date = ngày mai
        (Next Day)
        """
        res = super().default_get(fields_list)
        if 'start_date' in fields_list:
            from datetime import date, timedelta
            res['start_date'] = (
                date.today() + timedelta(days=1)
            ).isoformat()
        return res

    def name_get(self):
        """
        Custom display name: [Mã] Tên lớp - Ngày bắt đầu
        """
        result = []
        for record in self:
            if record.code and record.start_date:
                display_name = (
                    f"[{record.code}] {record.name} - "
                    f"{record.start_date.strftime('%d/%m/%Y')}"
                )
            elif record.code:
                display_name = f"[{record.code}] {record.name}"
            else:
                display_name = record.name
            result.append((record.id, display_name))
        return result

    def action_open(self):
        """
        Chuyển Draft -> Open. Kiểm tra phải có phòng học
        và giảng viên
        """
        for session in self:
            if not session.classroom_id:
                raise ValidationError(
                    'Phải chọn Phòng học trước khi mở đăng ký!'
                )
            if not session.instructor_id:
                raise ValidationError(
                    'Phải chọn Giảng viên trước khi mở đăng ký!'
                )
        self.write({'state': 'open'})

    def action_done(self):
        """Chuyển Open -> Done"""
        self.write({'state': 'done'})

    def action_cancel(self):
        """
        Chỉ cho hủy khi lớp chưa Done.
        Nếu Done -> raise UserError
        """
        for session in self:
            if session.state == 'done':
                raise UserError(
                    'Không thể hủy lớp học đã hoàn thành!'
                )
        self.write({'state': 'cancel'})

    def action_draft(self):
        """Đưa về trạng thái Draft"""
        self.write({'state': 'draft'})

    def copy(self, default=None):
        """
        Khi duplicate: Reset state về draft, xóa danh sách
        học viên, giữ khóa học
        """
        default = dict(default or {})
        default.update({
            'state': 'draft',
            'attendee_ids': [(5, 0, 0)],
        })
        return super(EduSession, self).copy(default)

    def unlink(self):
        """Chỉ cho xóa lớp ở trạng thái Draft hoặc Cancel"""
        for session in self:
            if session.state not in ('draft', 'cancel'):
                raise ValidationError(
                    f'Không thể xóa lớp "{session.name}" '
                    f'ở trạng thái "{session.state}"! '
                    'Chỉ được xóa lớp Dự thảo hoặc Hủy.'
                )
        return super(EduSession, self).unlink()

    @api.model
    def name_search(self, name='', args=None, operator='ilike',
                    limit=100):
        """Tìm kiếm nâng cao: theo Mã lớp hoặc Tên giảng viên"""
        args = args or []
        domain = []
        if name:
            domain = ['|', '|',
                      ('code', operator, name),
                      ('name', operator, name),
                      ('instructor_id.name', operator, name)]
        sessions = self.search(domain + args, limit=limit)
        return sessions.name_get()
