{
    'name': 'Finance Expense',
    'version': '1.0',
    'summary': 'Quản lý chi tiêu',
    'category': 'Accounting',
    'depends': ['base'],
    'data': [
        'security/finance_groups.xml',
        'security/finance_rules.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
