# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Customer Due Notification',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Show customer overdue amount warning in sales orders',
    'description': """
Customer Due Notification
=========================
This module shows customer overdue amount warning at the top of the sales order form.
A new group "Overdue Amount Viewer" is introduced. Only users in this group can see the actual overdue amount,
while other users will see a generic warning.
    """,
    'author': 'OdooLeap Solutions',
    'website': 'https://odooleap-solutions.odoo.com',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'account',
    ],
    'data': [
        'security/customer_due_notification_security.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
