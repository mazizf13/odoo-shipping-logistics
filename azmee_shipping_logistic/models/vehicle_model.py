from odoo import api, fields, models


class AzmeeVehicleModel(models.Model):
    _name = 'azmee.vehicle.model'
    _rec_name = 'name'
    _description = 'Azmee Vehicle Model'

    name = fields.Char()
    year_manufacture = fields.Char(string="Year", required=False, )
