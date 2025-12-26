# -*- coding: utf-8 -*-
# from odoo import http


# class Finance.expense(http.Controller):
#     @http.route('/finance.expense/finance.expense', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/finance.expense/finance.expense/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('finance.expense.listing', {
#             'root': '/finance.expense/finance.expense',
#             'objects': http.request.env['finance.expense.finance.expense'].search([]),
#         })

#     @http.route('/finance.expense/finance.expense/objects/<model("finance.expense.finance.expense"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('finance.expense.object', {
#             'object': obj
#         })

