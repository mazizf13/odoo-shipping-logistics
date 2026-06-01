from odoo import api, fields, models


class AzmeeVehicleBrand(models.Model):
    _name = 'azmee.vehicle.brand'
    _rec_name = 'name'
    _description = 'Azmee Vehicle Brand'

    name = fields.Char()
    vehicle_ids = fields.One2many(comodel_name="azmee.vehicle", inverse_name="brand_id", string="Vehicles", required=False, )