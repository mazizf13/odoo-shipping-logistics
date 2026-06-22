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
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id, )
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency")
    total = fields.Monetary(string="Total", )

    @api.onchange('line_ids')
    def onchange_line_ids(self):
        for me in self:
            total = 0
            for line in me.line_ids:
                total += line.subtotal
            me.total = total
        return

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('seq.shipment') or '/'
        return super(Shipment, self).create(vals_list)

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
    berat = fields.Float(string="Berat")
    harga = fields.Monetary(string="Harga")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", default=lambda self: self.env.user.company_id.id, )
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency")
    subtotal = fields.Monetary(string="Subtotal", compute="_compute_subtotoal")

    def _compute_subtotoal(self):
        for me in self:
            me.subtotal = me.berat * me.harga
        return

