from odoo import api, fields, models


class AzmeeVehicle(models.Model):
    _name = 'azmee.vehicle'
    _rec_name = 'name'
    _description = 'Azmee Vehicle'

    name = fields.Char()
    registration_number = fields.Char(string="Reg. Number", required=True, )
    notes = fields.Text()
    tyre_number = fields.Integer(required=True, )
    km = fields.Float()
    active = fields.Boolean(default=True)
    tax_expiry_date = fields.Date()
    last_inspection_time = fields.Datetime()
    condition = fields.Selection(selection=[
        ('normal', 'Normal'),
        ('need_easy_repair', 'Need Easy Repair'),
        ('need_hard_repair','Need Hard Repair')
    ], required=False, )
    brand_id = fields.Many2one(comodel_name="azmee.vehicle.brand", string="Brand", required=False, )
    model_id = fields.Many2one(comodel_name="azmee.vehicle.model", string="Model", required=False, )
    type_id = fields.Many2one(comodel_name="azmee.vehicle.type", string="Type", required=False, )
    year_manufacture = fields.Char(related="model_id.year_manufacture")

