# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    company_currency_id = fields.Many2one(
        related="company_id.currency_id",
        string="Company Currency",
        readonly=True,
    )
    overdue_amount = fields.Monetary(
        compute="_compute_overdue_amount",
        string="Overdue Amount",
        currency_field="company_currency_id",
        groups="customer_due_notification.group_overdue_amount_viewer",
        help="Outstanding overdue amount of the customer's commercial partner.",
    )
    has_overdue_amount = fields.Boolean(
        compute="_compute_overdue_amount",
        string="Has Overdue Amount",
        help="Technical field to check if customer has overdue amount.",
    )

    @api.depends("partner_id", "company_id")
    def _compute_overdue_amount(self) -> None:
        """Compute the overdue amount directly from account.move for commercial partner."""
        for order in self:
            commercial_partner = order.partner_id.commercial_partner_id
            if not commercial_partner:
                order.overdue_amount = 0.0
                order.has_overdue_amount = False
                continue

            today = fields.Date.context_today(self)

            # Query all overdue out invoices/refunds for the partner and children
            domain = [
                ("partner_id", "child_of", commercial_partner.id),
                ("invoice_date_due", "<", today),
                ("state", "=", "posted"),
                ("payment_state", "in", ("not_paid", "partial")),
                ("move_type", "in", ("out_invoice", "out_refund")),
                ("company_id", "=", order.company_id.id),
            ]
            groups = self.env["account.move"]._read_group(
                domain=domain,
                aggregates=["amount_residual_signed:sum"],
            )
            overdue_sum = groups[0][0] or 0.0
            # Ensure overdue amount is non-negative
            order.overdue_amount = max(overdue_sum, 0.0)
            order.has_overdue_amount = overdue_sum > 0.0
