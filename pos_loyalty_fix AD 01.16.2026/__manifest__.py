# pos_loyalty_fix/__manifest__.py
{
    'name': 'POS Loyalty Multi-Card Fix',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Prioritizes loyalty cards with the most points when a customer has multiple cards.',
    'description': """
        Fixes the issue where Odoo POS only reads the first loyalty card found for a partner.
        If a partner has multiple cards (e.g., one with 0 points and one with 1000 points),
        this module ensures the POS selects the card with the highest point balance.
    """,
    'depends': ['point_of_sale', 'pos_loyalty'],
    'data': [],
    'assets': {
        'point_of_sale.assets_prod': [
            'pos_loyalty_fix/static/src/js/pos_store_patch.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}