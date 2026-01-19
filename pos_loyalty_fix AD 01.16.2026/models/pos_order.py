# pos_loyalty_fix/models/pos_order.py
from odoo import models, api, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model_create_multi
    def create(self, vals_list):
        # 1. Create the orders as normal
        orders = super().create(vals_list)
        
        # 2. Run our rebalancing logic
        for order in orders:
            order._rebalance_loyalty_usage()
            
        return orders

    def _rebalance_loyalty_usage(self):
        """
        If a loyalty card was used and resulted in a negative balance,
        find other cards belonging to the same partner/program and
        transfer points to cover the deficit.
        """
        self.ensure_one()
        
        # Identify loyalty cards involved in this order
        # In Odoo 17, usage is often linked via coupon_id on lines
        used_coupons = self.lines.mapped('coupon_id')
        
        for card in used_coupons:
            # We only care about cards that have dropped below zero
            if card.points >= 0:
                continue

            # Calculate the deficit (e.g., points is -50, deficit is 50)
            deficit = abs(card.points)
            
            # Find 'sibling' cards: Same Partner, Same Program, Different ID, Positive Points
            sibling_cards = self.env['loyalty.card'].search([
                ('partner_id', '=', card.partner_id.id),
                ('program_id', '=', card.program_id.id),
                ('id', '!=', card.id),
                ('points', '>', 0)
            ], order='points desc') # Take from the richest card first

            for sibling in sibling_cards:
                if deficit <= 0:
                    break

                # How much can we take from this sibling?
                points_to_take = min(sibling.points, deficit)

                # Transfer the points
                # We simply adjust the points. Odoo's history tracking might not 
                # strictly log this transfer, but the balances will be correct.
                sibling.points -= points_to_take
                card.points += points_to_take
                
                deficit -= points_to_take

            # Optional: Log a note if we couldn't fully cover the deficit
            if deficit > 0:
                msg = f"POS Order {self.name}: Loyalty Card {card.code} is still negative (-{deficit}) after rebalancing attempt."
                self.env['ir.logging'].sudo().create({
                    'name': 'POS Loyalty Fix',
                    'type': 'server',
                    'level': 'warning',
                    'message': msg,
                    'path': 'pos_loyalty_fix',
                    'func': '_rebalance_loyalty_usage',
                    'line': '0',
                })