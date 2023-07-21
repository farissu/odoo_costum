# -*- coding: utf-8 -*-
{
    'name': "server",

    'summary': """
        Moduls Untuk Server""",

    'description': """
        menunjukan Ram & Disk Server
    """,

    'author': "farissu",
    'website': "https://bio.rizkifaris.repl.co/",

    'category': 'Management',
    'version': '0.1',

		# Depencicy
    'depends': ['base'],

		# Include ALL XML Code in Here be mindful of order
    'data': [
        'security/ir.model.access.csv',
        'views/menuitems.views.xml',
        'views/ticket_action.views.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False

}