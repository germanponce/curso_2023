# -*- coding: utf-8 -*-

# Clases Base para Odoo

from odoo import models, fields, api

class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Gestión de los Cursos Ofertados'
    _order = 'date_start'
    
    def _get_currency_company(self):
        print ("#### _get_currency_company >>>>>>>> ")

        current_user = self.env.user
        current_company = self.env.company
        print ("#### current_user: ", current_user)
        print ("#### usuario: ", current_user.login)
        print ("#### current_company: ", current_company)
        print ("#### moneda de la compañia: ", current_company.currency_id.name)

        currency_obj = self.env['res.currency'] # Instancia del objeto
        print ("#### currency_obj: ", currency_obj)
        # search = Busqueda
        # write = Escritura Valor
        # create = Crear un nuevo registro
        # read = Leer valores de un registro
        # search_read = Buscar y Leer

        currency_search_id = currency_obj.search([
                                                    ('name','=','MXN')
                                                  ], limit=1)

        print ("#### currency_search_id: ", currency_search_id)

        if currency_search_id:
            #### Siempre retorna solo  1 resultado #####
            return currency_search_id.id
            #### Si retorna mas de 1 resultado ########
            # return currency_search_id[0].id

        return False

    currency_id = fields.Many2one('res.currency', string="Moneda", default=_get_currency_company)

    company_id = fields.Many2one('res.company', string='Compañia', readonly=True, 
                                                default=lambda self: self.env.company)

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

    #### Campo Related ####
    photo = fields.Binary('Imagen', related="manager_id.image_1920")

    cost = fields.Monetary('Precio Unitario', digits=(14,2))

    #### Relacionales #####

    manager_id = fields.Many2one('res.users', 'Encargado')

    staff_id = fields.Many2one('res.users', 'Asistente')


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

