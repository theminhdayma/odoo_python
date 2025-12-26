{
    'name': 'Hồ sơ Ứng viên (Recruitment Simple)',
    'version': '1.0',
    'summary': 'Quản lý hồ sơ ứng viên đơn giản',
    'description': """
        Module quản lý ứng viên:
        - Lưu trữ thông tin ứng viên
        - Phân quyền Recruiter, Manager, Customer
        - Giao diện danh sách, form, search
    """,
    'category': 'Human Resources',
    'author': 'Antigravity',
    'depends': ['base', 'mail'],
    'data': [
        'security/hr_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_rules.xml',
        'views/hr_candidate_views.xml',
        'views/hr_candidate_menus.xml',
    ],
    'installable': True,
    'application': True,
}
