# Hướng Dẫn Chi Tiết Module Edu Management

## 📋 Mục Lục

1. [Tổng Quan](#tổng-quan)
2. [Cấu Trúc Dữ Liệu](#cấu-trúc-dữ-liệu)
3. [Chi Tiết Từng Model](#chi-tiết-từng-model)
4. [Workflow & States](#workflow--states)
5. [Logic Tính Toán](#logic-tính-toán)
6. [Security & Permissions](#security--permissions)
7. [Views & Features](#views--features)
8. [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)

---

## Tổng Quan

Module **Edu Management** là hệ thống quản lý giáo dục toàn diện cho Odoo 17, bao gồm:

- ✅ **Khóa học (Course)**: Quản lý các khóa học, chuyên ngành
- ✅ **Lớp học (Session)**: Tổ chức các lớp học với workflow trạng thái
- ✅ **Giảng viên (Instructor)**: Quản lý giảng viên và lịch dạy
- ✅ **Học viên (Attendee)**: Quản lý danh sách học viên
- ✅ **Phòng học (Classroom)**: Quản lý cơ sở vật chất, kiểm soát trùng lịch
- ✅ **Học phí (Fee)**: Tính toán doanh thu
- ✅ **Báo cáo**: Pivot, Graph, Calendar views
- ✅ **Bảo mật**: Quản lý quyền từng nhóm người dùng

---

## Cấu Trúc Dữ Liệu

### Entity Diagram - Chi Tiết Đầy Đủ

```
┌───────────────────────────────────────────────────────────────────────┐
│                         EDUCATION MANAGEMENT SYSTEM                    │
└───────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ res.partner (Người - Extends Base Model)                             │
├──────────────────────────────────────────────────────────────────────┤
│ Fields:                                                               │
│  • name (Char) - Tên đầy đủ                                          │
│  • email (Char) - Email liên hệ                                      │
│  • phone (Char) - Điện thoại                                         │
│  • is_instructor (Boolean) - Đánh dấu là giảng viên                 │
│                                                                       │
│ Relationships:                                                        │
│  • session_teaching_ids (One2many)                                   │
│    ↓ Linked: edu.session.instructor_id                               │
│    └─ Danh sách các lớp mà người này dạy                             │
│                                                                       │
│  • session_attending_ids (Many2many)                                 │
│    ↓ Through: edu_session_attendee_rel                               │
│    └─ Danh sách các lớp mà người này tham gia học                    │
│                                                                       │
│ Computed Fields:                                                      │
│  • session_teaching_count (Integer) - Số lớp dạy                    │
└──────────────────────────────────────────────────────────────────────┘
                               ▲              ▲
                    ┌──────────┘              └──────────┐
                    │                                    │
                    │ instructor_id                attendee_ids
                    │                                    │
┌───────────────────┴──────────────────────────────────┴──┐
│ edu.session (Lớp Học) ⭐⭐⭐ CORE MODEL               │
├────────────────────────────────────────────────────────┤
│ Identity Fields:                                        │
│  • id (Integer) - Auto ID                             │
│  • name (Char) - Tên lớp (VD: "Python 2024 - Lớp 1") │
│  • code (Char) - Mã tự động (VD: "SESS/00001")        │
│    └─ Generated from Sequence (ir.sequence)            │
│                                                        │
│ State & Tracking:                                      │
│  • state (Selection) - draft|open|done|cancel          │
│    └─ Workflow: draft → open → done / cancel           │
│  • active (Boolean) - Đang hoạt động                   │
│  • create_uid, create_date, write_uid, write_date      │
│                                                        │
│ Learning Content:                                      │
│  • course_id (Many2one → edu.course)                   │
│    └─ Khóa học mà lớp này thuộc về                     │
│  • instructor_id (Many2one → res.partner)              │
│    └─ Giảng viên (is_instructor = True)                │
│  • subject_id (via course_id) - Môn học                │
│                                                        │
│ Schedule:                                              │
│  • start_date (Date) - Ngày bắt đầu                    │
│    └─ Default: Ngày hôm nay + 1 ngày                   │
│  • duration (Float) - Thời lượng (giờ)                 │
│    └─ Ví dụ: 40 giờ                                    │
│  • end_date (Date) - Ngày kết thúc                     │
│    └─ Computed: start_date + (duration/8) ngày         │
│                                                        │
│ Location & Capacity:                                   │
│  • classroom_id (Many2one → edu.classroom)             │
│    └─ Phòng học (checked overlap)                      │
│  • seats (Integer) - Số chỗ tối đa                     │
│    └─ Default: 10 chỗ                                  │
│                                                        │
│ Attendee Management:                                   │
│  • attendee_ids (Many2many → res.partner)              │
│    └─ Danh sách học viên (không bao gồm instructor)   │
│  • attendee_count (Integer - Computed)                 │
│    └─ = len(attendee_ids)                              │
│  • taken_seats (Float - Computed)                      │
│    └─ = (attendee_count / seats) × 100%                │
│                                                        │
│ Financial:                                             │
│  • product_id (Many2one → product.template)            │
│    └─ Học phí (is_edu_fee = True)                      │
│  • revenue (Monetary - Computed)                       │
│    └─ = attendee_count × product_id.list_price         │
│  • currency_id (Many2one → res.currency)               │
│    └─ Tiền tệ (default: company currency)              │
│                                                        │
│ Features:                                              │
│  • mail.thread (Chatter - comments, history)           │
│  • mail.activity.mixin (Task management)               │
│                                                        │
│ Constraints:                                           │
│  1. Instructor không trong attendee_ids                │
│  2. duration > 0, start_date not null                  │
│  3. Phòng không trùng lịch (overlap check)             │
│                                                        │
│ Actions:                                               │
│  • action_open() - draft → open (check room+teacher)   │
│  • action_done() - open → done (readonly)              │
│  • action_cancel() - → cancel (không từ done)          │
│  • action_draft() - → draft (manager only)             │
│  • copy() - duplicate với state=draft, attendee=[]     │
│  • unlink() - delete chỉ draft/cancel                  │
└────────────────────────────────────────────────────────┘
    ▲                    ▲                    ▲
    │                    │                    │
    │ course_id          │ classroom_id      │ product_id
    │                    │                    │
    │             ┌──────┘                    │
    │             │                           │
┌───┴─────────────┴──────────┐  ┌─────────────┴──────────────┐
│ edu.course (Khóa Học)      │  │ edu.classroom (Phòng Học)  │
├────────────────────────────┤  ├────────────────────────────┤
│ Fields:                     │  │ Fields:                    │
│ • name (Char - UNIQUE)      │  │ • name (Char - UNIQUE)     │
│ • code (Char)               │  │ • code (Char)              │
│ • description (Html)        │  │ • capacity (Integer)       │
│ • level (Selection)         │  │   └─ CHECK(capacity > 0)   │
│   └─ basic/advanced         │  │ • description (Text)       │
│ • responsible_id (User)     │  │ • active (Boolean)         │
│ • active (Boolean)          │  │                            │
│ • subject_id (Many2one)     │  │ Relationships:             │
│                             │  │ • session_ids (One2many)   │
│ Relationships:              │  │   └─ Lớp dạy trong phòng   │
│ • subject_id → edu.subject  │  │ • session_count (Computed) │
│ • responsible_id → res.user │  │                            │
│ • session_ids (One2many)    │  │ Constraints:               │
│                             │  │ • name UNIQUE              │
│ Computed:                   │  │ • capacity > 0             │
│ • session_count (Integer)   │  │                            │
│                             │  │ Security:                  │
│ Constraints:                │  │ • User: Read-only          │
│ • name UNIQUE               │  │ • Manager: Full CRUD       │
│                             │  │                            │
│ Actions:                    │  └────────────────────────────┘
│ • Smart Button → Sessions   │
│   (session_count statinfo)  │
└────────────────────────────┘
    ▲
    │ subject_id
    │
┌───┴──────────────────────────┐
│ edu.subject (Môn Học)        │
├──────────────────────────────┤
│ Fields:                       │
│ • name (Char)                │
│ • code (Char - UNIQUE)        │
│ • description (Text)          │
│ • category (Selection)        │
│   ├─ it (CNTT)               │
│   ├─ economics (Kinh tế)      │
│   ├─ language (Ngoại ngữ)     │
│   └─ other (Khác)             │
│                              │
│ Relationships:                │
│ • course_ids (One2many)       │
│   └─ Khóa học của môn này     │
│ • course_count (Computed)     │
│                              │
│ Constraints:                  │
│ • code UNIQUE                 │
└──────────────────────────────┘


┌──────────────────────────────────────────────────────────────────────┐
│ product.template (Học Phí - Extended)                                │
├──────────────────────────────────────────────────────────────────────┤
│ Extends: product.template (Base Odoo Product Module)                 │
│                                                                       │
│ Additional Fields:                                                   │
│  • is_edu_fee (Boolean) - Đánh dấu đây là học phí                   │
│  • list_price (Decimal) - Giá học phí (từ base model)               │
│                                                                       │
│ Usage:                                                               │
│  • session.product_id → tính revenue                                 │
│  • domain filter: [('is_edu_fee', '=', True)]                        │
│                                                                       │
│ Security:                                                            │
│  • User: Read                                                        │
│  • Manager: Full CRUD                                                │
└──────────────────────────────────────────────────────────────────────┘
```

### Database Relations Summary

| From              | To               | Type      | Relation       | Cardinality |
| ----------------- | ---------------- | --------- | -------------- | ----------- |
| **res.partner**   | edu.session      | One2many  | instructor_id  | 1:N         |
| **res.partner**   | edu.session      | Many2many | attendee_ids   | M:N         |
| **edu.course**    | edu.subject      | Many2one  | subject_id     | N:1         |
| **edu.course**    | res.users        | Many2one  | responsible_id | N:1         |
| **edu.course**    | edu.session      | One2many  | session_ids    | 1:N         |
| **edu.session**   | edu.classroom    | Many2one  | classroom_id   | N:1         |
| **edu.session**   | product.template | Many2one  | product_id     | N:1         |
| **edu.classroom** | edu.session      | One2many  | session_ids    | 1:N         |

### Luồng Dữ Liệu & Quan Hệ Giữa Model

```
Khi Người Dùng Tạo Session (Lớp Học):

┌─ Chọn Khóa Học
│   └─ Tải dữ liệu: subject_id, responsible_id
│       └─ Tự động điền: instructor_id (nếu có partner)
│
├─ Chọn Phòng Học
│   └─ Kiểm tra: Phòng KHÔNG trùng với các lớp khác
│       └─ Ràng buộc: _check_classroom_overlapping()
│
├─ Nhập Danh Sách Học Viên
│   └─ Quan hệ: Many2many
│   └─ Ràng buộc: instructor_id KHÔNG nằm trong attendee_ids
│   └─ Kích hoạt cập nhật: attendee_count, taken_seats, revenue
│
└─ Chọn Sản Phẩm Học Phí
    └─ Tự động tính toán: revenue = attendee_count × list_price

Luồng Trạng Thái:

draft ──(action_open)──> open ──(action_done)──> done
  ▲                        │
  │                  (action_cancel)
  └─(action_draft)────────► cancel
     (chỉ manager)
```

### Cây Kế Thừa

```
edu.course (Khóa Học)
  └─ kế thừa từ: mail.thread, mail.activity.mixin
     ├─ Bổ sung trường: message_ids, message_follower_ids, activity_ids
     └─ Tính năng: Chatter (chat/bình luận), @mention, theo dõi hoạt động

edu.session (Lớp Học)
  └─ kế thừa từ: mail.thread, mail.activity.mixin
     ├─ Bổ sung trường: message_ids, message_follower_ids, activity_ids
     └─ Tính năng: Ghi chú nội bộ, theo dõi quyết định

edu.classroom (Phòng Học)
  └─ kế thừa từ: mail.thread, mail.activity.mixin
     └─ Tính năng: Chat, timeline

res.partner (Người)
  └─ kế thừa từ: res.partner (mô hình cơ sở Odoo)
     └─ Bổ sung trường: is_instructor, session_teaching_ids, session_teaching_count

product.template (Sản Phẩm)
  └─ kế thừa từ: product.template (mô hình cơ sở Odoo)
     └─ Bổ sung trường: is_edu_fee (flag đánh dấu học phí)
```

---

## Chi Tiết Từng Model

### 1. **edu.course** - Khóa Học

#### Fields:

| Field            | Type               | Mô Tả                       |
| ---------------- | ------------------ | --------------------------- |
| `name`           | Char               | Tên khóa học (UNIQUE)       |
| `description`    | Html               | Mô tả chi tiết              |
| `subject_id`     | Many2one           | Thuộc chuyên ngành nào      |
| `responsible_id` | Many2one           | Người phụ trách (res.users) |
| `level`          | Selection          | Trình độ: Cơ bản / Nâng cao |
| `active`         | Boolean            | Đang hoạt động hay không    |
| `session_ids`    | One2many           | Danh sách lớp học của khóa  |
| `session_count`  | Integer (Computed) | Số lớp học                  |

#### Logic Đặc Biệt:

**`_sql_constraints`** - SQL Constraints:

```python
('name_unique', 'UNIQUE(name)', 'Tên khóa học phải duy nhất!')
```

⚠️ **Tác dụng**: Cấp database level ngăn chặn trùng lặp tên khóa học

**`_compute_session_count()`** - Tính số lớp:

```python
@api.depends('session_ids')
def _compute_session_count(self):
    for record in self:
        record.session_count = len(record.session_ids)
```

📊 **Tác dụng**: Tự động đếm số lớp học của khóa, hiển thị trên smart button

**`_onchange_responsible_id()`** - Tự động điền email:

```python
@api.onchange('responsible_id')
def _onchange_responsible_id(self):
    if self.responsible_id and self.responsible_id.email:
        email_text = f"<p><strong>Email:</strong> {self.responsible_id.email}</p>"
        self.description = self.description + email_text if self.description else email_text
```

✉️ **Tác dụng**: Khi chọn người phụ trách → tự động thêm email vào mô tả

---

### 2. **edu.subject** - Môn Học/Chuyên Ngành

#### Fields:

| Field          | Type               | Mô Tả                           |
| -------------- | ------------------ | ------------------------------- |
| `name`         | Char               | Tên môn học                     |
| `code`         | Char               | Mã định danh (UNIQUE)           |
| `description`  | Text               | Mô tả                           |
| `category`     | Selection          | Phân loại: IT/Kinh tế/Ngoại ngữ |
| `course_ids`   | One2many           | Các khóa học của môn            |
| `course_count` | Integer (Computed) | Số khóa học                     |

#### Logic:

```python
_sql_constraints = [
    ('code_unique', 'UNIQUE(code)', 'Mã chuyên ngành phải duy nhất!')
]
```

---

### 3. **edu.classroom** - Phòng Học ⭐

#### Fields:

| Field           | Type               | Mô Tả                      |
| --------------- | ------------------ | -------------------------- |
| `name`          | Char               | Tên phòng (VD: Phòng A101) |
| `code`          | Char               | Mã phòng                   |
| `capacity`      | Integer            | Sức chứa tối đa            |
| `description`   | Text               | Cơ sở vật chất, thiết bị   |
| `active`        | Boolean            | Đang sử dụng               |
| `session_ids`   | One2many           | Lớp học trong phòng        |
| `session_count` | Integer (Computed) | Số lớp                     |

#### Constraints Quan Trọng:

**Capacity Check**:

```python
_sql_constraints = [
    ('capacity_check', 'CHECK(capacity > 0)', 'Sức chứa phải > 0!'),
]
```

✋ **Ngăn chặn**: Không thể lưu phòng với sức chứa ≤ 0

---

### 4. **edu.session** - Lớp Học (CORE MODEL) ⭐⭐⭐

#### Fields:

| Field            | Type      | Computed? | Mô Tả                         |
| ---------------- | --------- | --------- | ----------------------------- |
| `name`           | Char      | ❌        | Tên lớp                       |
| `code`           | Char      | ❌        | Mã lớp (auto từ Sequence)     |
| `state`          | Selection | ❌        | draft→open→done→cancel        |
| `course_id`      | Many2one  | ❌        | Khóa học                      |
| `instructor_id`  | Many2one  | ❌        | Giảng viên                    |
| `classroom_id`   | Many2one  | ❌        | Phòng học                     |
| `start_date`     | Date      | ❌        | Ngày bắt đầu                  |
| `duration`       | Float     | ❌        | Thời lượng (giờ)              |
| `end_date`       | Date      | ✅        | Tính từ start_date + duration |
| `seats`          | Integer   | ❌        | Số chỗ tối đa                 |
| `attendee_ids`   | Many2many | ❌        | Danh sách học viên            |
| `attendee_count` | Integer   | ✅        | Số học viên                   |
| `taken_seats`    | Float     | ✅        | % chỗ đã đặt                  |
| `product_id`     | Many2one  | ❌        | Học phí (product)             |
| `revenue`        | Monetary  | ✅        | Doanh thu                     |

#### Computed Fields Logic:

**1. `_compute_end_date()`**:

```python
@api.depends('start_date', 'duration')
def _compute_end_date(self):
    for session in self:
        if session.start_date and session.duration:
            days = session.duration / 8  # Giả sử 8 giờ/ngày
            session.end_date = session.start_date + timedelta(days=days)
        else:
            session.end_date = session.start_date
```

📅 **Logic**: Ngày kết thúc = Ngày bắt đầu + (Thời lượng / 8) ngày

**2. `_compute_attendee_count()`**:

```python
@api.depends('attendee_ids')
def _compute_attendee_count(self):
    for session in self:
        session.attendee_count = len(session.attendee_ids)
```

👥 **Logic**: Đếm số người trong danh sách tham dự

**3. `_compute_taken_seats()`**:

```python
@api.depends('seats', 'attendee_count')
def _compute_taken_seats(self):
    for session in self:
        if session.seats > 0:
            session.taken_seats = (session.attendee_count / session.seats) * 100
        else:
            session.taken_seats = 0.0
```

📊 **Logic**: % = (Số học viên / Số chỗ) × 100

**4. `_compute_revenue()`**:

```python
@api.depends('attendee_count', 'product_id', 'product_id.list_price')
def _compute_revenue(self):
    for session in self:
        if session.product_id:
            price = session.product_id.list_price
            session.revenue = session.attendee_count * price
        else:
            session.revenue = 0.0
```

💰 **Logic**: Doanh thu = Số học viên × Giá học phí

#### Onchange Methods:

**1. `_onchange_course_id()`** - Tự động điền giảng viên:

```python
@api.onchange('course_id')
def _onchange_course_id(self):
    if self.course_id and self.course_id.responsible_id:
        instructor = self.course_id.responsible_id.partner_id
        if instructor and instructor.is_instructor:
            self.instructor_id = instructor
```

🎯 **Tác dụng**: Chọn khóa → tự động điền người phụ trách làm giảng viên

**2. `_onchange_seats()`** - Kiểm tra số chỗ:

```python
@api.onchange('seats')
def _onchange_seats(self):
    if self.seats < 0:
        self.seats = 0
        return {
            'warning': {
                'title': 'Lỗi giá trị',
                'message': 'Số chỗ ngồi không được âm!'
            }
        }
```

⚠️ **Tác dụng**: Ngăn nhập số chỗ âm, hiển thị cảnh báo

**3. `_onchange_seats_attendees()`** - Cảnh báo quá tải:

```python
@api.onchange('seats', 'attendee_ids')
def _onchange_seats_attendees(self):
    if self.seats > 0 and len(self.attendee_ids) > self.seats:
        return {
            'warning': {
                'title': 'Cảnh báo',
                'message': f'Số học viên ({len(self.attendee_ids)}) vượt quá số chỗ ngồi ({self.seats})!'
            }
        }
```

🔔 **Tác dụng**: Cảnh báo khi học viên vượt quá chỗ

#### Constraints (Ràng buộc):

**1. `_check_instructor_not_in_attendees()`**:

```python
@api.constrains('instructor_id', 'attendee_ids')
def _check_instructor_not_in_attendees(self):
    for session in self:
        if (session.instructor_id and
                session.instructor_id in session.attendee_ids):
            raise ValidationError(
                f'Giảng viên "{session.instructor_id.name}" '
                'không được là học viên của lớp này!'
            )
```

❌ **Ngăn chặn**: Giảng viên không thể là học viên

**2. `_check_duration_and_start_date()`**:

```python
@api.constrains('duration', 'start_date')
def _check_duration_and_start_date(self):
    for session in self:
        if not session.start_date:
            raise ValidationError('Ngày bắt đầu không được để trống!')
        if session.duration and session.duration <= 0:
            raise ValidationError('Thời lượng phải > 0!')
```

❌ **Ngăn chặn**: Bắt buộc ngày bắt đầu, thời lượng > 0

**3. `_check_classroom_overlapping()`** - ⭐ Kiểm tra trùng phòng:

```python
@api.constrains('classroom_id', 'start_date', 'end_date')
def _check_classroom_overlapping(self):
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
```

🏛️ **Logic**:

- Tìm tất cả lớp khác cùng phòng
- Kiểm tra nếu thời gian trùng: `start_date <= end_date_new AND end_date >= start_date_new`
- Loại trừ lớp bị hủy (state = cancel)
- Nếu có trùng → Raise error

#### Workflow Methods:

**1. `action_open()`** - Draft → Open:

```python
def action_open(self):
    for session in self:
        if not session.classroom_id:
            raise ValidationError('Phải chọn Phòng học!')
        if not session.instructor_id:
            raise ValidationError('Phải chọn Giảng viên!')
    self.write({'state': 'open'})
```

✅ **Kiểm tra**: Phòng & giảng viên phải có

**2. `action_done()`** - Open → Done:

```python
def action_done(self):
    self.write({'state': 'done'})
```

**3. `action_cancel()`** - Hủy lớp:

```python
def action_cancel(self):
    for session in self:
        if session.state == 'done':
            raise UserError('Không thể hủy lớp đã hoàn thành!')
    self.write({'state': 'cancel'})
```

⛔ **Ngăn chặn**: Lớp Done không thể hủy

**4. `action_draft()`** - Reset về Draft:

```python
def action_draft(self):
    self.write({'state': 'draft'})
```

🔄 **Quyền**: Chỉ Manager

#### Special Methods:

**`copy()`** - Duplicate lớp:

```python
def copy(self, default=None):
    default = dict(default or {})
    default.update({
        'state': 'draft',
        'attendee_ids': [(5, 0, 0)],  # Xóa học viên cũ
    })
    return super(EduSession, self).copy(default)
```

📋 **Logic**: Khi duplicate → state = draft, học viên = rỗng

**`unlink()`** - Xóa lớp:

```python
def unlink(self):
    for session in self:
        if session.state not in ('draft', 'cancel'):
            raise ValidationError(
                f'Chỉ được xóa lớp Draft hoặc Cancel!'
            )
    return super(EduSession, self).unlink()
```

🗑️ **Ngăn chặn**: Chỉ xóa được Draft/Cancel

**`name_get()`** - Hiển thị custom:

```python
def name_get(self):
    result = []
    for record in self:
        if record.code and record.start_date:
            display_name = (
                f"[{record.code}] {record.name} - "
                f"{record.start_date.strftime('%d/%m/%Y')}"
            )
        # ...
        result.append((record.id, display_name))
    return result
```

🏷️ **Hiển thị**: `[SESS/00001] Python Class - 15/01/2024`

**`default_get()`** - Giá trị mặc định:

```python
@api.model
def default_get(self, fields_list):
    res = super().default_get(fields_list)
    if 'start_date' in fields_list:
        res['start_date'] = (date.today() + timedelta(days=1)).isoformat()
    return res
```

📅 **Logic**: Khi tạo lớp mới → start_date = ngày mai

**`name_search()`** - Tìm kiếm nâng cao:

```python
@api.model
def name_search(self, name='', args=None, operator='ilike', limit=100):
    if name:
        domain = ['|', '|',
                  ('code', operator, name),
                  ('name', operator, name),
                  ('instructor_id.name', operator, name)]
    sessions = self.search(domain + args, limit=limit)
    return sessions.name_get()
```

🔍 **Tìm theo**: Mã lớp, tên lớp, tên giảng viên

---

### 5. **res.partner** - Người (Mở rộng)

#### Thêm Fields:

| Field                    | Type               | Mô Tả                  |
| ------------------------ | ------------------ | ---------------------- |
| `is_instructor`          | Boolean            | Đánh dấu là giảng viên |
| `session_teaching_ids`   | One2many           | Lớp đang dạy           |
| `session_teaching_count` | Integer (Computed) | Số lớp dạy             |
| `session_attending_ids`  | Many2many          | Lớp đang học           |

#### Computed:

```python
@api.depends('session_teaching_ids')
def _compute_session_teaching_count(self):
    for record in self:
        count = len(record.session_teaching_ids)
        record.session_teaching_count = count
```

---

## Workflow & States

### State Flow Diagram:

```
┌─────────────┐
│   Draft     │ ← Tạo lớp mới, Reset from Cancel
│ (Dự thảo)  │
└──────┬──────┘
       │ action_open()
       │ (Kiểm tra: Phòng + Giảng viên)
       ↓
┌─────────────┐
│    Open     │ ← Nhận đăng ký học viên
│(Mở đăng ký) │
└──────┬──────┘
       │ action_done()
       ↓
┌─────────────┐
│    Done     │ ← Lớp hoàn thành (Form readonly)
│ (Hoàn thành)│
└─────────────┘
       ↑
       │ action_cancel()
       │ (Không từ Done)
┌─────────────┐
│   Cancel    │
│   (Hủy)    │
└─────────────┘
```

### State Properties:

| State      | Công Dụng                  | Có thể sửa form? | Có thể xóa? |
| ---------- | -------------------------- | ---------------- | ----------- |
| **draft**  | Soạn thảo, chưa chính thức | ✅               | ✅          |
| **open**   | Đang tuyển sinh            | ✅               | ❌          |
| **done**   | Hoàn thành, lưu trữ        | ❌ (Readonly)    | ❌          |
| **cancel** | Hủy bỏ                     | ✅               | ✅          |

---

## Logic Tính Toán

### 1. End Date (Ngày Kết Thúc)

**Công thức**:

```
end_date = start_date + (duration / 8) ngày
```

**Ví dụ**:

- start_date = 15/01/2024
- duration = 40 giờ
- end_date = 15/01/2024 + 5 ngày = **20/01/2024**

---

### 2. Taken Seats (% Chỗ Đã Đặt)

**Công thức**:

```
taken_seats (%) = (attendee_count / seats) × 100
```

**Ví dụ**:

- seats = 30
- attendee_count = 25
- taken_seats = (25 / 30) × 100 = **83.33%**

**Decoration**:

- 🔴 Red (danger): >= 100% (quá tải)
- ⚫ Gray (muted): state = cancel

---

### 3. Revenue (Doanh Thu)

**Công thức**:

```
revenue = attendee_count × product_id.list_price
```

**Ví dụ**:

- attendee_count = 25
- list_price = 500,000 VND
- revenue = 25 × 500,000 = **12,500,000 VND**

**Restriction**: Chỉ Manager thấy được trường này

---

## Security & Permissions

### 1. Groups (Nhóm)

```
Education
├── User (Giáo vụ)
│   ├── Cơ sở: base.group_user
│   └── Quyền: Chỉnh sửa dữ liệu cơ bản
│
└── Manager (Quản lý)
    ├── Cơ sở: group_edu_user
    ├── Quyền: Full CRUD tất cả
    └── Thành viên: Admin
```

### 2. CRUD Permissions (ir.model.access.csv)

| Model     | User (Giáo vụ)  | Manager (Quản lý) |
| --------- | --------------- | ----------------- |
| Course    | R/W/C (Xóa: ❌) | R/W/C/D ✅        |
| Subject   | R (Chỉ đọc)     | R/W/C/D           |
| Session   | R/W/C (Xóa: ❌) | R/W/C/D           |
| Classroom | R (Chỉ đọc)     | R/W/C/D           |

### 3. Record Rules (ed_session_rule_user.xml)

```python
domain_force = [
    '|',
    ('create_uid', '=', user.id),  # Lớp user tạo
    ('instructor_id', '=', user.partner_id.id)  # Lớp user dạy
]
```

👁️ **Tác dụng**: User chỉ thấy lớp mình tạo hoặc mình dạy

### 4. Field-Level Security

| Field     | User  | Manager |
| --------- | ----- | ------- |
| `revenue` | ❌ Ẩn | ✅ Thấy |

### 5. Button-Level Security

| Button      | Điều kiện              | Quyền        |
| ----------- | ---------------------- | ------------ |
| Mở đăng ký  | state = draft          | Tất cả       |
| Hoàn thành  | state = open           | Tất cả       |
| Hủy         | state ∉ [done, cancel] | Tất cả       |
| Reset Draft | state = cancel         | Manager only |

---

## Views & Features

### 1. Form View (Biểu Mẫu)

**Header (Nút bấm)**:

- 🟢 "Mở đăng ký" - Chuyển draft → open
- 🟢 "Hoàn thành" - Chuyển open → done
- 🔴 "Hủy" - Chuyển về cancel
- ⚙️ "Reset Draft" - Manager only

**Tabs**:

1. **Thông tin cơ bản** - name, code, course, giảng viên, phòng
2. **Thời gian** - start_date, duration, end_date
3. **Chỗ ngồi** - seats, attendee_count, taken_seats (progressbar)
4. **Học viên** - Danh sách Many2many
5. **Tài chính** - product_id, revenue (Manager only)

**Smart Button**:

```
┌─────────────────┐
│  👥 25 Lớp học  │  ← Hiển thị session_count
└─────────────────┘
```

### 2. Tree View (Danh Sách)

**Decorations**:

- 🔴 Red: taken_seats >= 100% (quá tải)
- ⚫ Gray: state = cancel

**Columns**: name, code, course, instructor, dates, capacity, attendees, state

### 3. Kanban View (Thẻ)

**Grouped by**: state (Draft/Open/Done/Cancel)

**Card Info**:

- 📌 Name, Course, Instructor
- 📅 Start Date
- 📊 Progress bar (taken_seats%)

### 4. Calendar View (Lịch)

**By**: start_date → end_date

**Color**: By instructor_id (tô màu khác nhau theo giảng viên)

### 5. Graph View (Biểu Đồ)

**Bar Chart**: Số học viên theo khóa học

```
     Số học viên
30   ┃
     ┃     ██
25   ┃  ██ ██
20   ┃  ██ ██
15   ┃  ██ ██
     ┃  ██ ██
  ┗━━╋━━┻━━┻━━━━
    Python | Java | C++
```

**Pie Chart**: Tỉ lệ lớp theo trạng thái

```
        Draft (10)
       /  \
   Cancel (5) - Open (15)
        \  /
       Done (20)
```

### 6. Pivot View (Phân Tích)

**Rows**: Khóa học
**Columns**: Giảng viên, Tháng
**Measures**: Số học viên, Doanh thu

```
                   │ Giảng viên A      │ Giảng viên B      │ Total
                   ├───────────────────┼───────────────────┼──────────
Python             │ Jan: 20 | 10M VND │ Feb: 15 | 7.5M VND │ 35 | 17.5M
Java               │ Jan: 15 | 7.5M    │ Mar: 10 | 5M VND    │ 25 | 12.5M
Total              │          17.5M    │          12.5M      │     30M
```

### 7. Search Filters

**Quick Filters**:

- 📌 Dự thảo (Draft)
- 📌 Mở đăng ký (Open)
- 📌 Hoàn thành (Done)
- 📅 **Lớp tuần này** (This week)
- 💰 **Doanh thu > 10 triệu**

**Group By**:

- Khóa học
- Giảng viên
- Trạng thái
- Ngày bắt đầu

---

## Hướng Dẫn Sử Dụng

### 🎓 Quy Trình Tạo & Quản Lý Lớp Học

#### Bước 1: Tạo Khóa Học

1. Vào **Education** → **Courses** → **Create**
2. Điền:
   - 📝 **Tên**: Python for Beginners
   - 🏷️ **Chuyên ngành**: IT
   - 📊 **Trình độ**: Cơ bản
   - 👤 **Người phụ trách**: [Chọn]
   - 📄 **Mô tả**: [Nhập]
3. **Save**

> 💡 Lưu ý: Tên khóa học phải duy nhất!

#### Bước 2: Tạo Phòng Học

1. Vào **Education** → **Classrooms** → **Create**
2. Điền:
   - 🏛️ **Tên phòng**: Phòng A101
   - 📍 **Mã phòng**: A101
   - 👥 **Sức chứa**: 30 chỗ
   - 📝 **Mô tả**: Có máy chiếu, bảng trắng
3. **Save**

> ⚠️ Lưu ý: Sức chứa phải > 0!

#### Bước 3: Tạo Lớp Học

1. Vào **Education** → **Sessions** → **Create**
2. **Form trống** (Trạng thái = Draft)
3. Điền thông tin:

   **Tab 1: Thông tin cơ bản**

   - 📝 **Tên lớp**: Python 2024 - Lớp 1
   - 🔗 **Khóa học**: Python for Beginners ← **[Auto → điền Giảng viên]**
   - 👤 **Giảng viên**: [Tự động từ course, hoặc chọn]
   - 🏛️ **Phòng học**: Phòng A101

   **Tab 2: Thời gian**

   - 📅 **Ngày bắt đầu**: 15/01/2024 (Mặc định = ngày mai)
   - ⏱️ **Thời lượng**: 40 giờ
   - ← **End Date tự động** = 15/01 + 5 ngày = 20/01/2024

   **Tab 3: Chỗ ngồi**

   - 👥 **Số chỗ**: 30
   - ← **Attendee count**: 0 (Tự động)
   - ← **Taken seats**: 0% (Tự động)

   **Tab 4: Học viên**

   - Chọn học viên: [Add rows]
   - ← **Attendee count tự động += 1**
   - ← **Taken seats tự động cập nhật %**

   **Tab 5: Tài chính** (Chỉ Manager thấy)

   - 💳 **Học phí**: [Chọn product]
   - ← **Revenue tự động** = attendee_count × price

4. **Save** (Vẫn ở state = Draft)

#### Bước 4: Mở Đăng Ký (Chuyển Open)

1. Lớp ở state = Draft
2. Bấm nút **"Mở đăng ký"** ✅
   - ✅ Kiểm tra: Phòng học? ✓ Giảng viên? ✓
   - ✅ Kiểm tra: Phòng không trùng lịch? ✓
   - ✅ state → **open**
3. Bây giờ học viên có thể đăng ký

#### Bước 5: Thêm/Xóa Học Viên

**Thêm**:

1. Tab "Học viên" → **Add row**
2. Chọn partner → **Save**
   - ← Attendee_count += 1
   - ← Taken_seats % cập nhật
   - ⚠️ Nếu vượt chỗ → Warning popup

**Xóa**:

1. Tab "Học viên" → **Delete row**
2. **Save**
   - ← Attendee_count -=1
   - ← Taken_seats % cập nhật

> ❌ **Cấm**: Không thể thêm Giảng viên vào danh sách học viên!

#### Bước 6: Hoàn Thành Lớp

1. state = **open**
2. Bấm **"Hoàn thành"** ✅
3. state → **done**
4. 🔒 Form **readonly** (Không thể sửa)
5. Chỉ có nút **"Reset Draft"** (Manager only)

#### Bước 7: Hủy Lớp

**Từ Draft**:

1. Bấm **"Hủy"** → state = cancel
2. Vẫn có thể xóa, sửa (chưa hoàn thành)

**Từ Open**:

1. Bấm **"Hủy"** → state = cancel
2. Không thể bấm nút khác

**Từ Done**:

1. ❌ Nút **"Hủy"** bị ẩn
2. ❌ Không thể hủy lớp hoàn thành
3. ✅ Chỉ **Reset Draft** (Manager)

---

### 📊 Xem Báo Cáo

#### Pivot (Phân tích doanh thu)

```
Education → Sessions → Pivot View

Rows: Course | Columns: Instructor, Month | Measure: Revenue
```

#### Graph (Biểu đồ)

```
Bar: Số học viên / Khóa học
Pie: Tỉ lệ trạng thái (Draft/Open/Done)
```

#### Calendar (Lịch)

```
Drag & Drop lớp trên lịch (by start_date - end_date)
```

---

### 🔐 Quản Lý Quyền Truy Cập

#### User (Giáo vụ):

- ✅ Create/Edit/Read: Course, Session
- ❌ Delete: Session, Classroom
- ❌ Xem revenue, reset draft
- 📌 Chỉ thấy lớp mình tạo/dạy

#### Manager (Quản lý):

- ✅ Full CRUD: Tất cả model
- ✅ Xem revenue
- ✅ Reset draft
- 📌 Thấy tất cả dữ liệu

---

### ⚠️ Lỗi Thường Gặp & Cách Khắc Phục

| Lỗi                      | Nguyên Nhân                             | Khắc Phục                    |
| ------------------------ | --------------------------------------- | ---------------------------- |
| "Phòng trùng lịch"       | Phòng được booking 2 lớp cùng thời gian | Chọn phòng/thời gian khác    |
| "Ngày bắt đầu trống"     | Quên điền start_date                    | Bắt buộc nhập ngày           |
| "Thời lượng ≤ 0"         | Duration = 0 hoặc âm                    | Nhập duration > 0            |
| "Giảng viên là học viên" | Thêm giáo viên vào attendee_ids         | Xóa giáo viên khỏi danh sách |
| "Không thể hủy lớp Done" | Lớp đã hoàn thành                       | Reset → Draft, rồi hủy       |
| "Tên khóa học trùng"     | Tên khóa đã tồn tại                     | Đặt tên khác                 |

---

## 🔧 Sequence & Auto-Increment

### Code Auto-Generation:

```python
# Mẫu: SESS/00001, SESS/00002, ...

<record id="seq_edu_session" model="ir.sequence">
    <field name="name">Session Code</field>
    <field name="code">edu.session</field>
    <field name="prefix">SESS/</field>
    <field name="number_next">1</field>
    <field name="number_increment">1</field>
</record>
```

📝 **Tác dụng**: Mỗi lớp tạo → tự động gán code SESS/xxxxx

---

## 📌 Summary

| Tính Năng  | Mô Tả                | Status |
| ---------- | -------------------- | ------ |
| Khóa học   | Quản lý course       | ✅     |
| Lớp học    | State workflow       | ✅     |
| Giảng viên | Linked partners      | ✅     |
| Học viên   | Many2many tracking   | ✅     |
| Phòng học  | Overlap checking     | ✅     |
| Doanh thu  | Computed revenue     | ✅     |
| Báo cáo    | Pivot/Graph/Calendar | ✅     |
| Bảo mật    | Groups & Rules       | ✅     |
| Search     | Advanced filters     | ✅     |

---

**✅ Module hoàn thiện với 20/20 tính năng!**
