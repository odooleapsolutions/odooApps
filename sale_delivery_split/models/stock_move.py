from odoo import models
from odoo.tools.float_utils import float_compare
from odoo.tools.misc import groupby


class StockMove(models.Model):
    _inherit = "stock.move"

    def _assign_picking(self):
        # Overriding.
        """ Try to assign the moves to an existing picking that has not been
        reserved yet and has the same procurement group, locations and picking
        type (moves should already have them identical). Otherwise, create a new
        picking to assign them to. """
        Picking = self.env['stock.picking']
        grouped_moves = groupby(self, key=lambda m: m._key_assign_picking())
        for group, moves in grouped_moves:
            moves = self.env['stock.move'].concat(*moves)
            new_picking = False
            # Could pass the arguments contained in group but they are the same
            # for each move that why moves[0] is acceptable
            picking = moves[0]._search_picking_for_assignation()
            if picking and not moves.sale_line_id.split_delivery:
                print("IF",moves)
                # If a picking is found, we'll append `move` to its move list and thus its
                # `partner_id` and `ref` field will refer to multiple records. In this
                # case, we chose to wipe them.
                vals = moves._assign_picking_values(picking)
                if vals:
                    picking.write(vals)
                moves.write({'picking_id': picking.id})
                moves._assign_picking_post_process(new=new_picking)
            else:
                # Additional Functionality :- First will create the picking for the non split items.
                # After that creating the picking for the split items.
                all_moves = self.env['stock.move'].concat(*moves)
                # Don't create picking for negative moves since they will be
                # reverse and assign to another picking
                grouped_moves = all_moves.filtered(
                    lambda l: not l.sale_line_id.split_delivery)
                print("grouped_moves 00",grouped_moves)
                grouped_moves = grouped_moves.filtered(
                    lambda m: float_compare(m.product_uom_qty, 0.0,
                                            precision_rounding=m.product_uom.rounding) >= 0)
                if grouped_moves:
                    new_picking = True
                    picking = Picking.create(
                        grouped_moves._get_new_picking_values())

                    grouped_moves.write({'picking_id': picking.id})
                    grouped_moves._assign_picking_post_process(new=new_picking)

                # Creating Picking for the splitting lines.

                grouped_moves = all_moves.filtered(
                    lambda l: l.sale_line_id.split_delivery)
                print("grouped_moves 01",grouped_moves)
                for item in grouped_moves:
                    item = item.filtered(
                        lambda m: float_compare(m.product_uom_qty, 0.0,
                                                precision_rounding=m.product_uom.rounding) >= 0)
                    if not item:
                        continue
                    new_picking = True
                    picking = Picking.create(
                        item._get_new_picking_values())
                    item.write({'picking_id': picking.id})
                    item._assign_picking_post_process(new=new_picking)
        return True
