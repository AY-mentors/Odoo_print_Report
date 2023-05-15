from odoo import fields, models, api


class CarData(models.Model):
    # _name = 'car.data'
    _inherit = ['product.template']
    _description = 'Data Of Invoice'

    date_from = fields.Date('Date from', required=True)
    date_to = fields.Date('Date to', required=True)

    standard_price = fields.Float(store=True)



    @api.depends_context('company')
    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_standard_price(self):
        # Depends on force_company context because standard_price is company_dependent
        # on the product_product
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.standard_price = template.product_variant_ids.standard_price
        for template in (self - unique_variants):
            template.standard_price = 0.0

# class TaxInherit(models.Model):
#     # _name = 'Tax Inherit'
#     _inherit = 'account.account'
#
#     tax_ids = fields.Many2many()



