{
    'name': 'Account Filter in Accounts Reports',
    'version': '18.0.0.0.1',
    'website': 'https://odooleap-solutions.odoo.com',
    'category': 'Accounting/Accounting',
    'author': 'OdooLeap Solutions',
    'depends': ['base', 'account_reports'],
    'description': """
            Account Filter in Accounting Reports
            ==================
        """,
    'assets': {
        'web.assets_backend': [
            'account_report_filter_account/static/src/xml/*',
            'account_report_filter_account/static/src/js/filter.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
