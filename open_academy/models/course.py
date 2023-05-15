# -*- coding: utf-8 -*-

# Clases Base para Odoo

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError


class Course(models.Model):
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
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


    def _get_compute_kanban(self):
        for rec in self:
            if not rec.manager_id and not rec.staff_id:
                rec.label_kaban = "Curso no disponible"
            else:
                rec.label_kaban = ""

    label_kaban = fields.Char('Etiqueta Kanban', compute="_get_compute_kanban")

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

    name = fields.Char('Nombre', size=128, required=True, index=True, tracking=1)

    date_start = fields.Date('Fecha Inicio', tracking=2)
    date_end = fields.Date('Fecha Fin', tracking=3)

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

    cost = fields.Monetary('Precio Unitario', tracking=1)

    #### Relacionales #####

    manager_id = fields.Many2one('res.users', 'Encargado')

    staff_id = fields.Many2one('res.users', 'Asistente')

    session_ids = fields.One2many('open_academy.session', 'course_id', 'Clases')

    no_copia = fields.Integer('No. de copia', copy=False)

    folio = fields.Char('Folio', size=64)

    ##### Restricciones de Odoo #####
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', "El nombre del curso debe ser unico"),
            ]

    @api.constrains('date_start','date_end')
    def _constraint_check_dates(self):
        for rec in self:
            if rec.date_end < rec.date_start:
                raise UserError("La fecha fin no puede ser mayor a la fecha de inicio.")
        return True
    

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


    #### herencia de funciones #####
    @api.model
    def create(self, vals):
        ### codigo antes ###
        ### self.env[''] -> Llamada a un modelo
        vals['folio'] = self.env['ir.sequence'].next_by_code('open_academy.course') or 'Nuevo'

        res = super(Course, self).create(vals)
        ### codigo despues ####
        return res


    def copy(self):
        ### codigo antes ###
        self.no_copia = self.no_copia + 1
        res = super().copy({'name':self.name+" (copia %s)" % self.no_copia})
        ### codigo despues ####
        return res

    def action_draft(self):
        self.state = 'draft'
        return True

    def action_pending(self):
        self.state = 'pending'
        return True

    def action_open(self):
        self.state = 'open'
        return True

    def action_in_process(self):
        self.state = 'in_process'
        return True

    def action_done(self):
        self.state = 'done'
        return True

    def action_cancel(self):
        self.state = 'cancel'
        body_html = "<h1>El registro <strong style='color:red'>%s</strong> fue cancelado.</h1>" % self.folio
        self.message_post(body=body_html)
        return True

    def action_view_sessions(self):
        # session_ids = []
        # for x in self.session_ids:
        #     session_ids.append(x.id)

        if not self.session_ids:
            raise ValidationError("No se tienen cursos registrados.")

        if self.session_ids:
            session_ids = [x.id for x in self.session_ids]

        return {
                    'domain': [('id', 'in', session_ids)],
                    'name': 'Sesiones del Curso %s' % self.folio,
                    'view_mode': 'tree,form',
                    'view_type': 'form',
                    'context': {'tree_view_ref': 'open_academy.session_tree'},
                    'res_model': 'open_academy.session',
                    'type': 'ir.actions.act_window'
                }