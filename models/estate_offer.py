# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError
import logging
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class estate_offer(models.Model):
  _name = 'estate.offer'
  _description = "Estate Offer"
  _order = "price desc"

  price = fields.Float(required = True)
  state = fields.Selection(
    string='State',
    selection=[('refused', 'Refused'), ('accepted', 'Accepted')],
    copy=False
  )
  partner_id = fields.Many2one('res.partner', required=True)
  property_id = fields.Many2one('estate.estate')

  property_type_id = fields.Many2one("estate.type", related="property_id.estate_type_id", store=True)

  validity = fields.Integer(default = 7)
  date_deadline = fields.Date(compute="_calculate_deadline", inverse = "_inverse_deadline")

  _sql_constraints = [
    ('check_offer_price', 'CHECK(price > 0.0)', 'Offer price must be strictly positive')
  ]

  @api.depends('validity')
  def _calculate_deadline(self):
    for record in self:
      record.date_deadline = fields.Date.today() + datetime.timedelta(days = record.validity)

  def _inverse_deadline(self):
    for record in self:
      delta = record.date_deadline - fields.Date.today()
      record.validity = delta.days
  
  def action_accept_offer(self):
    self.state = 'accepted'
    if (self.property_id):
      self.property_id.buyer_id = self.partner_id
      self.property_id.write({'selling_price': self.price})
      self.property_id.state = 'offer accepted'
      #self._check_percent()

  def action_refuse_offer(self):
    self.state = 'refused'

  @api.model
  def create(self, vals):
    if (len(self.env['estate.estate'].browse(vals['property_id']).offers_id) > 0):
      if (vals['price'] < min(map(lambda n: n.price, self.env['estate.estate'].browse(vals['property_id']).offers_id))):
        raise ValidationError("Offer's price is minimum")
    self.env['estate.estate'].browse(vals['property_id']).state = 'offer received'
    return super().create(vals)
