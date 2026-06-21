from odoo import api, fields, models

class WizardConfirmPLIssue(models.TransientModel):
    _name = 'wizard.confirm.pl.issue'
    _description = 'Wizard Confirm PL Issue'

    pl_issue_id = fields.Many2one(comodel_name="packing.list.issue", string="PL Issue", required=False, )
    warehouse_from_id = fields.Many2one(related="pl_issue_id.warehouse_from_id")
    warehouse_to_id = fields.Many2one(related="pl_issue_id.warehouse_to_id")

    def action_confirm(self):
        self.pl_issue_id.state = 'confirm'
        return