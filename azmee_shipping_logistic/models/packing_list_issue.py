from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PackingListIssue(models.Model):
    _name = 'packing.list.issue'
    _rec_name = 'name'
    _description = 'Packing List Issue'

    name = fields.Char(default='/', readonly=True)
    warehouse_from_id = fields.Many2one(comodel_name="stock.warehouse", string="From", required=True, )
    warehouse_to_id = fields.Many2one(comodel_name="stock.warehouse", string="To", required=True, )
    spb_ids = fields.Many2many(comodel_name="azmee.spb", string="SPB", domain=[('state', '=', 'approve'),])
    state = fields.Selection(string="Status", selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='draft', )
    line_ids = fields.One2many(comodel_name="packing.list.issue.line", inverse_name="pl_issue_id", string="Lines",)

    @api.onchange('spb_ids')
    def onchange_spb_ids(self):
        for me in self:
            data = [(5, 0, 0)] # Command 5 clears existing records
            if me.spb_ids:
                for spb in me.spb_ids:
                    for spb_line in spb.line_ids:
                        data.append((0, 0, {
                            'spb_id': spb.id,
                            'product_id': spb_line.product_id.id,
                            'qty_spb': spb_line.qty,
                            'qty_issue': spb_line.qty,
                        }))
            me.line_ids = data

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('seq.packing.list.issue') or '/'
        return super(PackingListIssue, self).create(vals_list)

    def action_confirm(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Confirmation PL Issue',
            'res_model': 'wizard.confirm.pl.issue',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_pl_issue_id': self.id},
            'views': [[False, 'form']]
        }

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
        return

class PackingListIssueLine(models.Model):
    _name = 'packing.list.issue.line'
    _description = 'Packing List Issue Line'

    pl_issue_id = fields.Many2one(comodel_name="packing.list.issue", string="PL Issue", required=False, ondelete="cascade")
    spb_id = fields.Many2one(comodel_name="azmee.spb", string="SPB", required=True, )
    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True, )
    qty_spb = fields.Float()
    qty_issue = fields.Float()

    @api.constrains('qty_issue')
    def check_qty(self):
        for me in self:
            if me.qty_issue > me.qty_spb:
                raise ValidationError("Qty issue tidak boleh lebih besar dari qty SPB")
        return
