from odoo import models, fields, api


class InvoicePDFReport(models.TransientModel):
    _name = 'sale.order.pdf.report'

    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')
    invoices = fields.Many2many('product.product', string='Products', required=False)

    # Generate xlsx report
    def action_generate_xlsx_report(self):

        domain = []
        domain_date = []
        invoice_id = self.invoices
        if invoice_id:
            domain += [('id', 'in', invoice_id.ids)]
        # date_from = self.date_from
        # if date_from:
        #     domain_date += [('date', '>=', date_from)]
        # date_to = self.date_to
        # if date_to:
        #     domain_date += [('date', '<=', date_to)]

        invoices = self.env['product.product'].search_read(domain)

        if invoices:
            data = {
                'invoices': invoices,
                # 'invoices_date': invoices_date,
                'form_data': self.read()[0],
            }
        return self.env.ref('tak_print_xlxs.report_invoice_data_xlsx_wizard').report_action(self, data=data)
