{
    'name': 'Salesperson Filter in Accounting Report',
    'version': '18.0.0.0.1',
    'website': 'https://odooleap-solutions.odoo.com',
    'category': 'Accounting/Accounting',
    'description': """
        SalesPerson Filter in Accounting Reports
        ==================
    """,
    'author': 'OdooLeap Solutions',
    'depends': ['base', 'account_reports'],
    'assets': {
        'web.assets_backend': [
            'account_report_filter_sales_person/static/src/xml/*',
            'account_report_filter_sales_person/static/src/js/filter.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
