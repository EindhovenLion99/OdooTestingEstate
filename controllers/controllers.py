# -*- coding: utf-8 -*-

from odoo import http

class Estate(http.Controller):
#     @http.route('/estate/estate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

     @http.route('/estates/<model("estate.estate"):estate>', auth='public', website=True)
     def getEstateById(self, estate):
       return http.request.render('estate.estate_id', {
         'estate': estate
       })
       #list = []

       #for estate in estates:
       #  n = {
       #    "name": estate.name,
       #    "id": estate.expected_price
       #  }
       #  list.append(n)

       #return list

     @http.route('/estates', auth="public", website=True)
     def getEstates(self, **kw):
       values = http.request.env['estate.estate'].search([])
       return http.request.render('estate.estates', {
         'values': values
       })


#     @http.route('/estate/estate/objects/<model("estate.estate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate.object', {
#             'object': obj
#         })
