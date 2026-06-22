import io
from fileinput import filename

import xlsxwriter
from datetime import datetime, time
from odoo import http
from odoo.http import content_disposition, request

class ControllerShippingReport(http.Controller):
    @http.route('/azmee-shipping/report/<int:wizard_id>', type='http', auth='user')
    def download_shipping_report(self, wizard_id, **kw):
        wizard = request.env['wizard.shipping.report'].browse(int(wizard_id))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Shipping Report")

        row = 0
        col = 0
        worksheet.write(row, col, "From Date")
        col += 1
        worksheet.write(row, col, wizard.date_from.strftime("%d/%m/%Y"))
        row += 1

        col = 0
        worksheet.write(row, col, 'To Date')
        col += 1
        worksheet.write(row, col, wizard.date_to.strftime("%d/%m/%Y"))

        row += 1
        col = 0
        worksheet.write(row, col, 'No SPB')
        data = request.env['azmee.spb'].search([
            ('transfer_date', '>=', wizard.date_from),
            ('transfer_date', '<=', wizard.date_to),
        ])

        for line in data:
            row += 1
            worksheet.write(row, col, line.name)

        workbook.close()
        output.seek(0)

        filename = f'shipping_report.xlsx'

        return request.make_response(output.read(), headers=[
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', content_disposition(filename)),
        ])