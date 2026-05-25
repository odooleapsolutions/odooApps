# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import tagged

from odoo.addons.sale.tests.common import TestSaleCommon


@tagged('post_install', '-at_install')
class TestSaleOrderDueNotification(TestSaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a group for overdue amount viewers
        cls.group_viewer = cls.env.ref('customer_due_notification.group_overdue_amount_viewer')

        # Create users for testing access control
        cls.viewer_user = cls.env['res.users'].create({
            'name': 'Viewer Salesperson',
            'login': 'viewer_salesperson',
            'email': 'viewer@example.com',
            'group_ids': [Command.link(cls.env.ref('sales_team.group_sale_salesman').id),
                          Command.link(cls.group_viewer.id)],
        })

        cls.non_viewer_user = cls.env['res.users'].create({
            'name': 'Regular Salesperson',
            'login': 'regular_salesperson',
            'email': 'regular@example.com',
            'group_ids': [Command.link(cls.env.ref('sales_team.group_sale_salesman').id)],
        })

    def test_overdue_amount_computation_and_child_aggregation(self):
        """Test that sale.order overdue amount computes correctly and aggregates children."""
        partner = self.partner_a
        child_partner = self.env['res.partner'].create({
            'name': 'Child Contact',
            'parent_id': partner.id,
            'type': 'invoice',
        })

        # Create a sales order
        order = self.env['sale.order'].create({
            'partner_id': partner.id,
        })

        # Initially overdue amount should be 0.0
        order.invalidate_recordset(['overdue_amount', 'has_overdue_amount'])
        self.assertEqual(order.sudo().overdue_amount, 0.0)
        self.assertFalse(order.has_overdue_amount)

        # Create a posted invoice in the past for the parent
        invoice_parent = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': '2020-01-01',
            'date': '2020-01-01',
            'invoice_line_ids': [Command.create({
                'name': 'parent test line',
                'quantity': 1,
                'price_unit': 400.0,
                'tax_ids': False,
            })],
        })
        invoice_parent.action_post()

        # Create a posted invoice in the past for the child contact
        invoice_child = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': child_partner.id,
            'invoice_date': '2020-01-01',
            'date': '2020-01-01',
            'invoice_line_ids': [Command.create({
                'name': 'child test line',
                'quantity': 1,
                'price_unit': 300.0,
                'tax_ids': False,
            })],
        })
        invoice_child.action_post()

        # Recalculate order overdue amount
        order.invalidate_recordset(['overdue_amount', 'has_overdue_amount'])
        self.assertEqual(order.sudo().overdue_amount, 700.0)
        self.assertTrue(order.has_overdue_amount)

    def test_sale_order_overdue_warning_and_security(self):
        """Test sales order flag has_overdue_amount and view permissions."""
        partner = self.partner_a

        # Create a posted invoice in the past
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': '2020-01-01',
            'date': '2020-01-01',
            'invoice_line_ids': [Command.create({
                'name': 'test line',
                'quantity': 1,
                'price_unit': 500.0,
                'tax_ids': False,
            })],
        })
        invoice.action_post()

        # Create a sales order
        order = self.env['sale.order'].create({
            'partner_id': partner.id,
        })

        # Verify computed boolean flag is True
        order.invalidate_recordset(['has_overdue_amount', 'overdue_amount'])
        self.assertTrue(order.has_overdue_amount)

        # Access with the viewer user (must see the correct overdue amount)
        order_viewer = order.with_user(self.viewer_user)
        self.assertEqual(order_viewer.overdue_amount, 500.0)

        # Access with the non-viewer user (must raise AccessError)
        order_non_viewer = order.with_user(self.non_viewer_user)
        with self.assertRaises(AccessError):
            _ = order_non_viewer.overdue_amount
