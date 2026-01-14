/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    getLoyaltyCardForPartner(program, partner) {
        const allCards = Object.values(this.loyalty_cards || {});

        const matchingCards = allCards.filter(card =>
            card.program_id === program.id &&
            card.partner_id &&
            card.partner_id.id === partner.id
        );

        if (matchingCards.length === 0) {
            return null;
        }
        // 1. Sum up ALL points from all cards
        const totalPoints = matchingCards.reduce((sum, card) => sum + card.points, 0);

        // 2. Sort by ID descending (use the newest card as the 'Host')
        matchingCards.sort((a, b) => b.id - a.id);
        const bestCard = matchingCards[0];

        // 3. Clone the card to avoid modifying the real data
        const proxyCard = Object.assign(Object.create(Object.getPrototypeOf(bestCard)), bestCard);

        // 4. Overwrite points with the total sum
        proxyCard.points = totalPoints;

        return proxyCard;
    },

    get_loyalty_card_by_program_id(program_id) {
        const order = this.get_order();
        const partner = order ? order.get_partner() : null;

        if (!partner) {
            return super.get_loyalty_card_by_program_id(...arguments);
        }

        const program = this.models['loyalty.program'].get(program_id);

        if (program) {
            const bestCard = this.getLoyaltyCardForPartner(program, partner);
            if (bestCard) {
                return bestCard;
            }
        }

        return super.get_loyalty_card_by_program_id(...arguments);
    }
});