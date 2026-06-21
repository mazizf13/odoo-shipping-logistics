from email.policy import default

from odoo import api, fields, models

class Shipment(models.Model):
    _name = 'azmee.shipment'
    _rec_name = 'name'
    _description = 'Shipment'

    name = fields.Char(default='/', readonly=True)
    driver_name = fields.Char()
    vehicle_id = fields.Many2one(comodel_name='azmee.vehicle', string="Vehicle", required=False)
    departure_date = fields.Datetime(default=fields.Date.today())
    line_ids = fields.One2many(comodel_name="azmee.shipment.line", inverse_name="shipment_id", string="Lines")
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], default='draft', required=True)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val['name'] = self.env['ir.sequence'].next_by_code('seq.shipment')
        return super(Shipment, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
        return

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
        return

class ShipmentLine(models.Model):
    _name = 'azmee.shipment.line'
    _description = 'Shipment Line'

    shipment_id = fields.Many2one(comodel_name="azmee.shipment", string="Shipment", required=False, )
    pl_issue_id = fields.Many2one(comodel_name="packing.list.issue", string="PL Issue", required=False, )
    state = fields.Selection(string="Status Issue", selection=[
        ('draft', 'Draft'),
        ('on_progress', 'On Progress'),
        ('received', 'Received'),
        ('problem', 'Problem'),
    ], default='draft', required=False, )

