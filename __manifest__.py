{
    'name': 'Xlsx Print Data',
    'version': '16.1.1',
    'summary': 'Summery',
    'description': 'Description',
    'category': 'Category',
    'author': 'Car',
    'website': 'Website',
    'license': 'AGPL-3',
    'sequence': -100,
    'depends': ['report_xlsx', 'sale_management', 'account_accountant', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/invoice_view_wizard.xml',
        'views/invoice_inherit_view.xml',
        'report/report.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
