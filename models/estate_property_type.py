# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class estate_type(models.Model):
  _name = 'estate.type'
  _description = "Estate Type"
  _order = "name"

  name = fields.Char(required = True)

  offer_ids = fields.One2many('estate.offer', 'property_type_id', string="Offer")
  offer_count = fields.Integer(compute="_countOffers")

  property_id = fields.One2many('estate.estate', 'estate_type_id', string=_("Property"))

  _sql_constraints = [
    ('check_name_unique', 'UNIQUE (name)', 'Type must be unique')
  ]

  @api.depends("offer_ids")
  def _countOffers(self):
    for record in self:
      record.offer_count = len(record.offer_ids)
