# custom_sales_order/__manifest__.py
{
    'name': 'Custom Sales Order Fields',
    'version': '1.0',
    'summary': 'Adds custom fields to Sales Order',
    'author': 'Your Name',
    'depends': ['sale'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
}
