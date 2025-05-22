from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    split_delivery = fields.Boolean(string="Split Delivery",
                                    help="Create Separate Delivery order for this particular Product.")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    split_all = fields.Boolean(string="Split All",
                               help="Create Separate Delivery for all the lines.")

    @api.onchange('split_all')
    def _onchange_split_all(self):
        for rec in self.order_line.filtered(lambda l: not l.is_delivery):
            rec.write({'split_delivery': self.split_all})
