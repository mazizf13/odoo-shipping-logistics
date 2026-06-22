from odoo import api, fields, models


class WizardShippingReport(models.TransientModel):
    _name = 'wizard.shipping.report'
    _description = 'Wizard Shipping Report'

    date_from = fields.Date('From Date')
    date_to = fields.Date('To Date')

    def action_print(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'azmee-shipping/report/{self.id}',
            'target': 'self',
        }

