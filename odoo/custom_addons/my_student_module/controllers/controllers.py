# -*- coding: utf-8 -*-
# from odoo import http


# class MyStudentModule(http.Controller):
#     @http.route('/my_student_module/my_student_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_student_module/my_student_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_student_module.listing', {
#             'root': '/my_student_module/my_student_module',
#             'objects': http.request.env['my_student_module.my_student_module'].search([]),
#         })

#     @http.route('/my_student_module/my_student_module/objects/<model("my_student_module.my_student_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_student_module.object', {
#             'object': obj
#         })

