# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EduClassroom(models.Model):
    _name = 'edu.classroom'
    _description = 'Phòng học (Classroom)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(
        string='Tên Phòng',
        required=True,
        tracking=True,
        help='VD: Phòng A101, Phòng C202'
    )
    code = fields.Char(
        string='Mã Phòng',
        tracking=True,
        help='Mã phòng (VD: A101)'
    )
    capacity = fields.Integer(
        string='Sức chứa tối đa',
        required=True,
        default=30,
        tracking=True,
        help='Số chỗ ngồi tối đa của phòng'
    )
    description = fields.Text(
        string='Mô tả',
        help='Mô tả về cơ sở vật chất, thiết bị'
    )
    active = fields.Boolean(
        string='Đang sử dụng',
        default=True,
        tracking=True
    )
    session_ids = fields.One2many(
        'edu.session',
        'classroom_id',
        string='Danh sách Lớp'
    )
    session_count = fields.Integer(
        string='Số lớp',
        compute='_compute_session_count',
        store=True
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tên phòng phải duy nhất!'),
        ('capacity_check', 'CHECK(capacity > 0)',
         'Sức chứa phải lớn hơn 0!'),
    ]

    @api.depends('session_ids')
    def _compute_session_count(self):
        for record in self:
            record.session_count = len(record.session_ids)

    @api.constrains('capacity')
    def _check_capacity(self):
        """Validate sức chứa > 0"""
        for record in self:
            if record.capacity <= 0:
                raise ValueError('Sức chứa phòng phải lớn hơn 0!')
