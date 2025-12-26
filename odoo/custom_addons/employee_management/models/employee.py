from odoo import fields, models


class Employee(models.Model):
    _name = 'employee.management.employee'
    _description = 'Employee'

    position_choices = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('hr', 'HR'),
    ]

    name = fields.Char(string='Name', required=True)
    position = fields.Selection(selection=position_choices, string='Position', required=True)
    salary = fields.Float(string='Salary', default=1000.0, required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today, required=True)

