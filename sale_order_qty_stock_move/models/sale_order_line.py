from datetime import timedelta

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, values):
        res = super().write(values)
        if (
            "customer_lead" in values
            and self.state == "sale"
            and not self.order_id.commitment_date
        ):
            # Propagate deadline on related stock move
            self.move_ids.date_deadline = self.order_id.date_order + timedelta(
                days=self.customer_lead or 0.0
            )
        return res
