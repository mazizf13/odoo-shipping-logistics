import typing

from odoo import api, fields, models
from odoo.exceptions import UserError


class PackingListReceipt(models.Model):
    _name = "packing.list.receipt"
    _rec_name = "name"
    _description = "Packing List Receipt"

    name = fields.Char(default="/", readonly=True)
    receiver_name = fields.Char()
    receiver_date = fields.Datetime(default=fields.Date.today())
    line_ids = fields.One2many(comodel_name="packing.list.receipt.line", inverse_name="pl_receipt_id", string="Lines", required=False, )
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], default='draft', required=False, )
    shipment_ids = fields.Many2many(comodel_name="azmee.shipment", string="Shipments")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('seq.packing.list.receipt') or '/'
        return super(PackingListReceipt, self).create(vals_list)

    def unlink(self):
        for me in self:
            if me.state != 'draft':
                raise UserError("Tidak boleh delete dokumen PL Receipt yang sudah done")
        return super(PackingListReceipt, self).unlink()

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return

    @api.onchange('shipment_ids')
    def onchange_shipment_ids(self):
        for me in self:
            data = [(5, 0, 0)]
            if me.shipment_ids:
                for shipment in me.shipment_ids:
                    for shipment_line in shipment.line_ids:
                        for pl_issue_line in shipment_line.pl_issue_id.line_ids:
                            data.append((0, 0, {
                                'pl_issue_line_id': pl_issue_line.id,
                            }))
            me.line_ids = data

class PackingListReceiptLine(models.Model):
    _name = "packing.list.receipt.line"
    _description = "Packing List Receipt Line"

    pl_receipt_id = fields.Many2one(comodel_name="packing.list.receipt", string="Packing List Receipt", required=False)
    pl_issue_line_id = fields.Many2one(comodel_name="packing.list.issue.line", string="Packing List Issue Line", required=False, )
    pl_issue_id = fields.Many2one(related="pl_issue_line_id.pl_issue_id", string="PL Issue")
    spb_id = fields.Many2one(related="pl_issue_line_id.spb_id", string="SPB")
    product_id = fields.Many2one(related="pl_issue_line_id.product_id", string="Product")
    qty_spb = fields.Float(related="pl_issue_line_id.qty_spb", )
    qty_issue = fields.Float(related="pl_issue_line_id.qty_issue", )
    qty_receipt = fields.Float()