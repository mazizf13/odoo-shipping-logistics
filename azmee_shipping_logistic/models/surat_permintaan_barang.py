from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SPB(models.Model):
    _name = 'azmee.spb'
    _rec_name = 'name'
    _description = 'SPB'

    name = fields.Char(default='/', readonly=True)
    transfer_date = fields.Datetime(default=fields.Date.today())
    warehouse_from_id = fields.Many2one(comodel_name="stock.warehouse", string="From", required=True, )
    warehouse_to_id = fields.Many2one(comodel_name="stock.warehouse", string="To", required=True, )
    line_ids = fields.One2many(comodel_name="azmee.spb.lines", inverse_name="spb_id", string="Lines", required=False, )
    total_qty = fields.Float(string="Total Quantity", compute="_compute_total_qty")
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ], default='draft', )

    @api.constrains('line_ids')
    def _check_qty(self):
        for me in self:
            if not me.line_ids:
                raise ValidationError("Isikan daftar barang!")
            for line in me.line_ids:
                if not line.product_id or line.qty < 1:
                    raise ValidationError("Isikan product dan qty dengan benar!")
        return

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    def action_reject(self):
        for rec in self:
            rec.state = 'reject'

    @api.depends('line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(rec.line_ids.mapped('qty'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env.ref('azmee_shipping_logistic.seq_azmee_spb').next_by_id() or '/'
        return super(SPB, self).create(vals_list)

class SPBLines(models.Model):
    _name = 'azmee.spb.lines'
    _description = 'SPB Lines'

    spb_id = fields.Many2one(comodel_name="azmee.spb", string="SPB", required=False, )
    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True, )
    qty = fields.Float(string="Quantity")

    @api.constrains('qty')
    def _check_qty_max_limit(self):
        for rec in self:
            if rec.qty > 100:
                raise ValidationError("Qty tidak boleh lebih dari 100")


