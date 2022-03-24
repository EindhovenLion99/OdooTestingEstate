# -*- coding: utf-8 -*-

from odoo import http

class Estate(http.Controller):

     @http.route('/estates/<model("estate.estate"):estate>', auth='public', website=True)
     def getEstateById(self, estate):
       return http.request.render('estate.estate_id', {
         'estate': estate
       })

     @http.route('/estates', auth="public", website=True)
     def getEstates(self, **kw):
       values = http.request.env['estate.estate'].search([])
       return http.request.render('estate.estates', {
         'values': values
       })
