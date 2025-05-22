{
    'name': 'Sale Delivery Split',
    'version': '18.0.0.0.1',
    'website': 'https://odooleap-solutions.odoo.com',
    'category': 'Sale',
    'description': """
        SaleOrder Delivery Order Split
        ==================
    """,
    'author': 'OdooLeap Solutions',
    'depends': ['sale', 'sale_management', 'stock'],
    'data': [
        'views/sale_order_view.xml'
    ],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
