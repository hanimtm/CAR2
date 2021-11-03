# -*- coding: utf-8 -*-

{
    'name': 'Purchase Order - Import',
    'author': 'Aneesh.AV',
    'category': 'Extra Tools',
    'summary': 'Purchase Order - Import',
    'description': '''
        Purchase Order - Import
                    ''',
    'version': '15.0.1',
    'depends': ['purchase','product','stock'],
    'application': True,
    'data': [
        'security/import_po_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_po_wizard.xml',
        'wizard/import_message_wizard.xml',
        'wizard/import_inventory_wizard.xml',
        'views/product.xml',
        'views/purchase_view.xml',
        'views/stock_picking.xml',
        'views/res_config_settings.xml'
    ],
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
