# -*- coding: utf-8 -*-
{
    'name': "estate",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        
        'security/security.xml',
        'security/rule.xml',
        'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'views/tableViewEstate.xml',
        'views/menus.xml',
        'views/viewsEstate.xml',
        'views/viewsOffer.xml',
        'views/viewsTypes.xml',
        'views/viewsTags.xml',
        'views/tableViewOffer.xml',
        'views/tableViewType.xml',
        'views/tableViewTag.xml',
        'views/formEstate.xml',
        'views/formOffer.xml',
        'views/formType.xml',
        'views/searchEstate.xml',
        'views/formUser.xml',
        'views/viewsUsers.xml',
        'views/kanbanEstate.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
