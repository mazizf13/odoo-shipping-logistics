from odoo import api, fields, models


class AzmeeVehicleType(models.Model):
    _name = 'azmee.vehicle.type'
    _rec_name = 'name'
    _description = 'Azmee Vehicle Type'

    name = fields.Char()
