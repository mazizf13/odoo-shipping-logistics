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
        col += 1
        worksheet.write(row, col, 'No PL Issue')
        col += 1
        worksheet.write(row, col, 'No Shipment')
        col += 1
        worksheet.write(row, col, 'No PL Receipt')
        col += 1
        worksheet.write(row, col, 'Product Name')

        query = '''
                    SELECT
                        spb.id                            AS spb_id,
                        spb.name                          AS spb_number,

                        pli.id                            AS pl_issue_line_id,
                        pli_hdr.id                        AS pl_issue_id,
                        pli_hdr.name                      AS pl_issue_number,

                        ship.id                           AS shipment_id,
                        ship.name                         AS shipment_number,

                        pr.id                             AS pl_receipt_id,
                        pr.name                           AS pl_receipt_number,

                        pp.id                             AS product_id,
                        pt.name                           AS product_name,

                        pli.qty_spb,
                        pli.qty_issue,
                        prl.qty_receipt

                    FROM azmee_spb spb

                    INNER JOIN packing_list_issue_line pli
                           ON pli.spb_id = spb.id

                    INNER JOIN packing_list_issue pli_hdr
                           ON pli_hdr.id = pli.pl_issue_id

                    INNER JOIN azmee_shipment_line sl
                           ON sl.pl_issue_id = pli_hdr.id

                    INNER JOIN azmee_shipment ship
                           ON ship.id = sl.shipment_id

                    INNER JOIN packing_list_receipt_line prl
                           ON prl.pl_issue_line_id = pli.id

                    INNER JOIN packing_list_receipt pr
                           ON pr.id = prl.pl_receipt_id

                    INNER JOIN product_product pp
                           ON pp.id = pli.product_id

                    INNER JOIN product_template pt
                           ON pt.id = pp.product_tmpl_id
                '''
        domain_list = []
        params = []
        if wizard.date_from:
            domain_list.append("spb.transfer_date >= %s")
            params.append(wizard.date_from)
        if wizard.date_to:
            domain_list.append("spb.transfer_date <= %s")
            params.append(wizard.date_to)
        if domain_list:
            domain_str = " and ".join(domain_list)
            query += "where " + domain_str
        query += '''
                ORDER BY
                        spb.name,
                        pli_hdr.name,
                        ship.name,
                        pr.name;
                '''
        request.env.cr.execute(query, tuple(params))
        data = request.env.cr.dictfetchall()
        for line in data:
            row += 1
            col = 0
            worksheet.write(row, col, line["spb_number"])
            col += 1
            worksheet.write(row, col, line["pl_issue_number"])
            col += 1
            worksheet.write(row, col, line["shipment_number"])
            col += 1
            worksheet.write(row, col, line["pl_receipt_number"])
            col += 1
            worksheet.write(row, col, line["product_name"].get('en_US', ''))

        # data = request.env['azmee.spb'].search([
        #     ('transfer_date', '>=', wizard.date_from),
        #     ('transfer_date', '<=', wizard.date_to),
        # ])
        #
        # for line in data:
        #     row += 1
        #     worksheet.write(row, col, line.name)

        workbook.close()
        output.seek(0)

        filename = f'shipping_report.xlsx'

        return request.make_response(output.read(), headers=[
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', content_disposition(filename)),
        ])