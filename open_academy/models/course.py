# -*- coding: utf-8 -*-

# Clases Base para Odoo

from odoo import models, fields, api

class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Gestión de los Cursos Ofertados'
    _order = 'date_start'

    state  = fields.Selection([
                                ('draft','Borrador'),
                                ('pending','Pendiente'),
                                ('open','Abierto'),
                                ('in_process','En proceso'),
                                ('done','Finalizado'),
                                ('cancel', 'Cancelado'),
                              ], string="Estado", default="draft")

    name = fields.Char('Nombre', size=128, required=True, index=True)

    date_start = fields.Date('Fecha Inicio')
    date_end = fields.Date('Fecha Fin')

    active = fields.Boolean('Activo', default=True)

    description = fields.Html('Información Curso')

    notes = fields.Text('Notas')

    duration = fields.Integer('Duración')

    course_type = fields.Selection([
                                    ('online','En linea'),
                                    ('presential', 'Presencial'),
                                  ], 'Tipo de Curso')

    photo = fields.Binary('Imagen')

    cost = fields.Float('Precio Unitario', digits=(14,2))

    #### Relacionales #####

    # # Tipos # #
    #  Char
    #  Float
    #  Boolean
    #  Date
    #  Datetime
    #  Int
    #  Text
    #  Html
    #  Binary

    # # Relacionales
    #  Many2one
    #  One2many
    #  Many2many
    #  Related

    # # Calculados
    #  Function
