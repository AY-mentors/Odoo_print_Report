import datetime as datetime

from odoo import models


class InvoiceDataXlsxWizard(models.AbstractModel):
    _name = 'report.tak_print_xlxs.invoice_xlsx_report_wizard'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, cars):

        data_header = ['التاريخ', 'الشهر', 'رقم الفاتورة', 'دفتر اليوميه', 'الفرع', 'العميل','مركز التكلفه','Group','اسم الصنف','الكمية','السعر','القيمة','سعر التكلفه','نسبة الخصم','قيمة التكلفة','قيمة الخصم',
                       'السعر بعد الخصم','نسبة الضريبة','قيمة الضريبة','الصافي']

        len_data = len(data_header)

        report_name = "الفواتير"
        header_format = workbook.add_format({
            "valign": "vcenter",
            "align": "center",
            "bg_color": "#951F06",
            "bold": True,
            'font_color': '#FFFFFF',
            'border': 1,
            'border_color': ''  # D3D3D3'
        })
        cell_format = workbook.add_format({
            "valign": "vcenter",
            "align": "center",
            "bold": True,
        })
        date_style = workbook.add_format({"valign": "vcenter", "align": "center", "bold": True, 'num_format': 'dd-mm-yyyy'})
        date_style_2 = workbook.add_format({"valign": "vcenter", "align": "center", "bold": True, 'num_format': 'dd-mm'})
        # One sheet by partner
        worksheet = workbook.add_worksheet(report_name[:31])
        worksheet.right_to_left()
        # bold = workbook.add_format({'bold': True})
        worksheet.set_zoom(90)
        worksheet.set_column('A:Q', 20)

        row = 0
        col = 0

        for rec in range(len_data):
            worksheet.write(row, col, data_header[rec], header_format)
            col += 1

        date_from = data['form_data']['date_from']
        date_to = data['form_data']['date_to']

        get_ids = []
        len_data_id = len(data['invoices'])

        for rec in range(len_data_id):
            get_ids.append(data['invoices'][rec]['id'])


        d = tuple(get_ids + [0])

        # (select DISTINCT  account_analytic_account.partner_id where account_analytic_account.partner_id in (10) ) )
        # (select account_analytic_account.partner_id from account_analytic_account GROUP BY partner_id  HAVING COUNT(distinct partner_id) > 1))
        # (select account_analytic_account.id from account_analytic_account) as ddd

        query = 'Select distinct (quantity * price_unit) as qema,' \
                '(select distinct name from account_journal where id = account_move_line.journal_id) as account_name' \
                ', (account_move_line.quantity * product_template.standard_price) as get_q, ' \
                ' account_move.amount_tax' \
                ', account_move.date, account_move_line.name, account_move.amount_tax_signed, account_move.amount_total_signed, account_move_line.analytic_distribution, account_move_line.discount_percentage, ' \
                'account_move_line.quantity, (product_category.name) as caregory_name, product_template.standard_price, product_template.categ_id, account_move_line.discount,account_move_line.price_unit' \
                ',account_move_line.move_name,account_move.state,(res_partner.name) as partner_branch, res_partner.parent_id, (select distinct res_partner.name from res_partner where res_partner.id in (select distinct res_partner.parent_id from res_partner where res_partner.id in (account_move.partner_id))) as par_name ' \
                'from product_product inner join account_move_line ON account_move_line.product_id in' + str(d) + ''\
                'INNER JOIN account_move ON account_move_line.move_id in  (select distinct move_id from account_move_line)' \
                'INNER JOIN product_template ON product_template.id in ((select distinct product_tmpl_id from product_product where product_product.id = account_move_line.product_id)) ' \
                'INNER JOIN product_category ON product_category.id in (product_template.categ_id) ' \
                'INNER JOIN res_partner ON res_partner.id in (account_move.partner_id) ' \
                ' WHERE  CAST(account_move.date as date) between CAST ('"' "+str(date_from)+" '"' as date) and CAST('"'"+str(date_to)+"'"' as date)''' \
                # 'GROUP BY account_move_line.product_id'
        # (select res_partner.name where res_partner.id in (res_partner.parent_id)) as par_name

        self.env.cr.execute(query)
        invoices_query = self.env.cr.dictfetchall()

        get_dest = []
        add_num = []
        get_len_anl = len(invoices_query)

        row = 1
        for rec in range(get_len_anl):
            get_dest.append(invoices_query[rec]['analytic_distribution'])

        analytic_id = len(get_dest)
        for rec in range(analytic_id):
            add_num.append(get_dest[rec])

        lllkk = len(add_num)
        for rec in range(lllkk):
            result_2 = [int(x) for x in add_num[rec]]
            result_23 = []
            result_23.append(result_2)

        iii = len(result_23)
        for rec in range(iii):
            show_analytic_id = self.env['account.analytic.account'].browse(result_23[rec]).mapped('name')
            show_analytic_id_2 = []
            show_analytic_id_2.append(show_analytic_id)
            worksheet.write(row, 6, '"' + str(show_analytic_id_2[1]) + ', ' '"', cell_format)
            row += 1
        # for rec in show_analytic_id:
        #     var_data = rec


        # lll = len(show_analytic_id)
        # for rec in range(lll):
        #     all_names = []
        #     # all_names.append(name_add[rec][rec]['name'])
        #     # pppp = len(all_names)
        #     # for rec in range(pppp):
        #     # worksheet.write(row, 6, '"' + str(all_names[0]) + ', "', cell_format)
        #     worksheet.write(row, 6, '"' + show_analytic_id[rec] + ', "', cell_format)
        #     row += 1



        # result_2 = [int(x) for x in show_analytic_id]
        #
        # len_number = []
        # for rec in result_2:
        #     len_number.append(rec)
        #
        #     get_len_id = len(len_number)
        #     for rec in range(get_len_id):
        #         get_id_par = self.env['account.analytic.account'].search_read([('id', 'in', [len_number[0]])])
        #         # get_id_par_2 = self.env['account.analytic.account'].search_read([('id', 'in', [add_nnn[1]])])
        #         name_add = []
        #         name_add.append(get_id_par)
        #
        #     len_all_name = len(name_add)
        #     for rec in range(len_all_name):
        #         all_names = []
        #         all_names.append(name_add[rec][rec]['name'])
        #         # pppp = len(all_names)
        #         # for rec in range(pppp):
        #         # worksheet.write(row, 6, '"' + str(all_names[0]) + ', "', cell_format)
        #         worksheet.write(row, 6, '"' + str(all_names[0]) + ', "', cell_format)
        #     row += 1


        qema_precentage = []
        discountsss_precentage = []
        lll = len(invoices_query)

        for rec in range(lll):
            qema = invoices_query[rec]['qema']
            qema_precentage.append(qema)

            discount_percentage_data = invoices_query[rec]['discount_percentage']
            discountsss_precentage.append(discount_percentage_data)

        col = 0
        row = 1

        len_data = len(invoices_query)

        for obj in range(len_data):
            worksheet.write(row, 0, invoices_query[obj]['date'], date_style)
            # if get_new[obj] != 0:
            worksheet.write(row, 1, invoices_query[obj]['date'], date_style_2)
            worksheet.write(row, 2, invoices_query[obj]['move_name'], cell_format)
            worksheet.write(row, 3, invoices_query[obj]['account_name'], cell_format)
            worksheet.write(row, 4, invoices_query[obj]['partner_branch'], cell_format)
            worksheet.write(row, 5, invoices_query[obj]['par_name'], cell_format)
            # worksheet.write(row, 6, invoices_query[obj]['analytic_distribution']['6'], cell_format)
            # worksheet.write(row, 6, '"' + show_analytic_id[0] + ', ' + show_analytic_id[1] + '"', cell_format)
            # worksheet.write(row, 6, '"' + show_analytic_id[obj] + ', ' '"', cell_format)
            # worksheet.write(row, 6, '"'+get_id_par[0]['name']+', '+''+get_id_par[1]['name']+'"', cell_format)
            # worksheet.write(row, 6, 'مركز التكلفة', cell_format)
            worksheet.write(row, 7, invoices_query[obj]['caregory_name'], cell_format)
            worksheet.write(row, 8, invoices_query[obj]['name'], cell_format)
            worksheet.write(row, 9, invoices_query[obj]['quantity'], cell_format)
            worksheet.write(row, 10, invoices_query[obj]['price_unit'], cell_format)
            worksheet.write(row, 11, invoices_query[obj]['qema'], cell_format)
            worksheet.write(row, 12, invoices_query[obj]['standard_price'], cell_format)
            if invoices_query[obj]['discount_percentage'] != None:
                worksheet.write(row, 13, invoices_query[obj]['discount_percentage'], cell_format)
            else:
                worksheet.write(row, 13, 0, cell_format)
            worksheet.write(row, 14, invoices_query[obj]['get_q'], cell_format)
            if discountsss_precentage[0] != None:
                worksheet.write(row, 15, qema_precentage[0] * discountsss_precentage[0], cell_format)
            else:
                worksheet.write(row, 15, qema_precentage[0] * 0, cell_format)
            if discountsss_precentage[0] != None:
                worksheet.write(row, 16, (qema_precentage[obj] - (qema_precentage[obj] * discountsss_precentage[0])),
                                cell_format)
            else:
                worksheet.write(row, 16, (qema_precentage[obj] - (qema_precentage[obj] * 0)), cell_format)
            worksheet.write(row, 17, 0.14, cell_format)
            # if discountsss_precentage[0] != None:
            #     worksheet.write(row, 18, (qema_precentage[obj] - (qema_precentage[obj] * discountsss_precentage[0])) *  invoices_query[obj]['amount_tax_signed'],
            #                     cell_format)
            # else:
            #     worksheet.write(row, 18, (qema_precentage[obj] - (qema_precentage[obj] * 0)) * invoices_query[obj]['amount_tax_signed'], cell_format)

            worksheet.write(row, 18, invoices_query[obj]['amount_tax_signed'], cell_format)
            worksheet.write(row, 19, invoices_query[obj]['amount_total_signed'], cell_format)

            # if discountsss_precentage[0] != None:
            #     worksheet.write(row, 19,
            #                     ((qema_precentage[obj] - (qema_precentage[obj] * discountsss_precentage[0])) * invoices_query[obj]['amount_tax_signed']) +
            #                     (qema_precentage[obj] - (qema_precentage[obj] * discountsss_precentage[0])),
            #                     cell_format)
            # else:
            #     worksheet.write(row, 19, ((qema_precentage[obj] - (qema_precentage[obj] * 0)) * invoices_query[obj]['amount_tax_signed']) +
            #                     (qema_precentage[obj] - (qema_precentage[obj] * 0)), cell_format)
            # col += 1
            row += 1
