# -*- coding: utf-8 -*-

{
    'name': 'Openacademy Curso 2023',
    'version': '0.1',
    'author': 'German Ponce Dominguez',
    'website': 'http://poncesoft.blogspot.com',
    'category': 'Capacitacion',
    'summary': 'Desarrollo de formularios para capacitacion de desarrollo.',
    'description': """

Este modulo agrega una seria de formularios para entender el desarrollo de la API de Odoo V15

    """,
    'depends': ['base'],

    'data': [
                # Vistas #
                'views/course_view.xml',
                'views/menu.xml',
                # Permisos de Acceso #
                'security/ir.model.access.csv',
                # Datos Demo #
                'data/demo.xml',
                'data/open_academy.course.csv',
            ],

    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'assets': {
    },
    'license': 'LGPL-3',
}
