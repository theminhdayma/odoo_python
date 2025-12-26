# -*- coding: utf-8 -*-

from odoo import models, fields


class FinanceExpense(models.Model):
    _name = "finance.expense"
    _description = "Yêu cầu chi tiêu"

    name = fields.Char(
        string="Tên khoản chi",
        required=True
    )

    expense_type = fields.Selection(
        selection=[
            ('travel', 'Di chuyển'),
            ('food', 'Ăn uống'),
            ('other', 'Khác')
        ],
        string="Loại chi phí",
        default='travel',
        required=True
    )

    amount = fields.Float(
        string="Số tiền",
        required=True
    )

    expense_date = fields.Date(
        string="Ngày chi tiêu",
        default=fields.Date.today
    )

    is_paid = fields.Boolean(
        string="Đã thanh toán",
        default=False
    )

    approval_note = fields.Text(
        string="Ghi chú duyệt chi",
        groups="finance_expense.group_finance_manager"
    )
