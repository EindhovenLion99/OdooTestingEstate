# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class estate(models.Model):
  _name = 'estate.estate'
  _description = 'Estates'
  _order = 'id desc'

  name = fields.Char(required = True)
  description = fields.Text()
  postcode = fields.Char()
  state = fields.Selection(
    string='State',
    selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
    help="State is used to indicate New, Sold or Cancelled", default = "new")
  date_availability = fields.Date(default = fields.Date.today() + relativedelta(months = 3))
  expected_price = fields.Float(required = True)
  selling_price = fields.Float()
  bedrooms = fields.Integer(default = 2)
  living_area = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean(default = False)
  garden = fields.Boolean(default = False)
  garden_area = fields.Integer()
  garden_orientation = fields.Selection(
    string='Type',
    selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')],
    help="Type is used to indicate North, South, West or East")

  active = fields.Boolean(default = True)
  
  estate_type_id = fields.Many2one('estate.type', string="Type")

  tag_ids = fields.Many2many('estate.tag', string="Tags")

  buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
  salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)

  offers_id = fields.One2many('estate.offer', 'property_id', required=True)
  total_area = fields.Float(compute="_total_area")

  company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.user.company_id)

  _sql_constraints = [
    ('check_name_unique', 'UNIQUE (name)', 'Unique Name'),
    ('check_expected_price', 'CHECK(expected_price > 0.0)', 'Expected price must be strictly positive'),
    ('check_sellin_price', 'CHECK(selling_price >= 0.0)', 'Selling price must be positive')
  ]

  @api.depends('living_area', 'garden_area')
  def _total_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area
  
  best_offer = fields.Float(compute="_best_offer")

  @api.depends('offers_id')
  def _best_offer(self):
    for record in self:
      if record.offers_id:
        record.best_offer = max(record.offers_id.mapped('price'))
      else:
        record.best_offer = 0


  @api.onchange("garden")
  def _onchange_garden(self):
    if self.garden:
      self.garden_area = 10
      self.garden_orientation = 'north'
    else:
      self.garden_area = 0
      self.garden_orientation = ''


  def action_sell_status(self):
    for record in self:
      try:
          a = record.check_access_rule('write')
          _logger.info("REACHED " + str(a))
      except:
          raise UserError("Error")
      if (record.state == 'new' or record.state == 'offer received' or record.state == 'offer accepted'):
        record.state = 'sold'
      elif (record.state == 'cancelled'):
        raise UserError('Cancelled properties can not be sold')
      else:
        raise UserError('Property already sold')
    return True

  def action_cancel_status(self):
    for record in self:
      if (record.state == 'new'):
        record.state = 'cancelled'
      elif (record.state == 'sold' or record.state == 'offer received' or record.state == 'offer accepted'):
        raise UserError('Sold properties or with current offer can not be cancelled')
      else:
        raise UserError('Property already cancelled')
    return True

  @api.constrains('selling_price')
  def _check_percent(self):
    for record in self:
      if (record.selling_price < record.expected_price * 0.9 and record.selling_price > 0.0):
        raise ValidationError("Best offer must be at least 90 percent of selling price")

  acceptedOffer = fields.Boolean(compute = "_anyAcceptedOffer")

  @api.depends('offers_id')
  def _anyAcceptedOffer(self):
    for record in self:
      record.acceptedOffer = False
      for offer in record.offers_id:
        if offer.state == 'accepted':
          record.acceptedOffer = True

  @api.onchange('offers_id')
  def _updateState(self):
    if len(self.offers_id) > 0:
      self.state = 'offer received'

  def unlink(self):
    for record in self:
      if (record.state == 'offer received' or record.state == 'offer accepted'):
          raise UserError("You can not delete a property in states Offer Received or Offer Accepted")
    return super(estate, self).unlink()


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
