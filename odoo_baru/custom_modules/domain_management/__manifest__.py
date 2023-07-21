{
    'name': "Domain",

    'summary': """
        Module Monitoring Domain Cinte""",

    'description': """
        Manajemen Monitoring Domain Cinte
    """,

    'author': "Muhammad Dwi Prasetyo",
    'website': "https::/cinte.id",

    'category': 'Uncategorized',
    'version': '0.1',

		# Depencicy
    'depends': ['base'],

		# Include ALL XML Code in Here be mindful of order
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/menuitems.views.xml',
        'views/main.views.xml',
        'views/subdomain.views.xml',
        'views/report.views.xml',
        'views/config/bot.views.xml',
        'views/config/management.views.xml',
        'views/config/ownership.views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False

}