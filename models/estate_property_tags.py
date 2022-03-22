# -*- coding: utf-8 -*-

from odoo import models, fields, api

class estate_tags(models.Model):
  _name = 'estate.tag'
  _description = "Estate Tag"

  name = fields.Char(required = True)

  sequence = fields.Integer('Sequence', default=1)

  color = fields.Integer()

  _sql_constraints = [
    ('check_name_unique', 'UNIQUE (name)', 'Tag must be unique')
  ]