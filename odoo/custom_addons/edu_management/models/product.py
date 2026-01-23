
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_edu_fee = fields.Boolean(
        string='Là Học phí',
        default=False,
        tracking=True,
        help='Đánh dấu nếu sản phẩm này là học phí của khóa học'
    )
    list_price = fields.Float(
        string='Giá niêm yết',
        help='Giá học phí'
    )
