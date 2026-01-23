# -*- coding: utf-8 -*-
{
    'name': "edu_management",
    'summary': """
        Education Management System
        Quản lý Khóa học, Môn học, Lớp học và Học viên""",
    'description': """
        Module quản lý đào tạo:
        - Quản lý Khóa học (Courses)
        - Quản lý Môn học/Chuyên ngành (Subjects)
        - Quản lý Giảng viên (Instructors)
        - Quản lý Học phí (Education Fees)
        - Tích hợp với Product và Partner
    """,
    'author': "Your Company",
    'website': "https://www.yourcompany.com",
    'category': 'Education',
    'version': '17.0.1.0.0',
    'depends': ['base', 'product'],
    'data': [
        'security/edu_security.xml',
        'security/ir.model.access.csv',
        'security/edu_session_rule_user.xml',
        'data/ir_sequence_data.xml',
        'views/edu_actions.xml',
        'views/edu_course_views.xml',
        'views/edu_subject_views.xml',
        'views/edu_session_views.xml',
        'views/edu_classroom_views.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/edu_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
