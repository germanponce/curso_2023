# -*- coding: utf-8 -*-

# Clases Base para Odoo

from odoo import models, fields, api
from random import randint

class SessionTag(models.Model):
    _name = "open_academy.session.tag"
    _description = 'Etiquetas de Sesiones'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Nombre', size=64)
    color = fields.Integer('Color', default=_get_default_color)

class Session(models.Model):
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _name = "open_academy.session"
    _description = 'Sesiones del Curso'
    
    def _current_datetime(self):
        return fields.Datetime.now()

    @api.depends('number_of_seats', 'attendace_ids')
    def _get_takens_free(self):
        for rec in self:
            number_of_attendances = len(rec.attendace_ids)
            number_of_seats_free = rec.number_of_seats - number_of_attendances
            print ("#### number_of_seats_free: ", number_of_seats_free)
            rec.number_of_seats_free = number_of_seats_free

    @api.depends('number_of_seats', 'attendace_ids')
    def _get_taken_seats_percent(self):
        for rec in self:
            number_of_attendances = len(rec.attendace_ids)
            number_of_seats = rec.number_of_seats
            number_of_seats_percent = 0.0
            number_of_seats_disponibility = 100
            if number_of_attendances and number_of_seats:
                number_of_seats_percent = 100 * (number_of_attendances / number_of_seats)
                number_of_seats_disponibility = 100 - number_of_seats_percent
            rec.number_of_seats_percent = number_of_seats_percent
            rec.number_of_seats_disponibility = number_of_seats_disponibility

    name = fields.Char('Descripción', size=128, required=True)
    initial_date = fields.Datetime('Fecha Inicio', default=_current_datetime)
    end_date = fields.Datetime('Fecha Fin')
    number_of_seats = fields.Integer('# Lugares')
    instructor_id = fields.Many2one('res.partner', 'Instructor')
    
    attendace_ids = fields.Many2many('res.partner', 
                                     'sessions_attendances_rel', 'session_id', 'partner_id',
                                     'Asistentes')

    tag_ids = fields.Many2many('open_academy.session.tag', 
                                     'sessions_tags_rel', 'session_id', 'tag_id',
                                     'Etiquetas')

    color = fields.Integer('Color')

    course_id = fields.Many2one('open_academy.course', 'Curso/ID Ref',
                                help="Asocia la clase al curso...", ondelete="cascade")

    number_of_seats_free = fields.Integer('# Lugares Disponibles', compute="_get_takens_free")

    number_of_seats_percent = fields.Float('Cupo lleno al', digits=(3,2), compute="_get_taken_seats_percent")

    number_of_seats_disponibility = fields.Float('Disponibilidad', digits=(3,2), compute="_get_taken_seats_percent")

    maximum_rate = fields.Integer('Rate Max.', default=100)

    no_copia = fields.Integer('No. de copia', copy=False)

    folio = fields.Char('Folio', size=64)
    #### Query Consulta de Union de Tablas ####
    """ 
        select oas.name, rp.name nombre_sesion from open_academy_session as oas
                                   join sessions_attendances_rel as sar
                                     on sar.session_id = oas.id
                                   join res_partner as rp
                                     on rp.id = sar.partner_id
    """

    @api.onchange('number_of_seats', 'attendace_ids')
    def onchange_number_of_seats(self):
        if self.number_of_seats and self.attendace_ids:
            number_of_attendances = len(self.attendace_ids)
            number_of_seats_free = self.number_of_seats - number_of_attendances
            print ("########### number_of_seats_free:", number_of_seats_free)
            if number_of_seats_free < 0:
                number_of_attendances = self.number_of_seats + abs(number_of_seats_free)
                print ("########### number_of_attendances:", number_of_attendances)
                self.number_of_seats = number_of_attendances
                return {
                            'warning': {
                                'title': "Advertencia!!!!",
                                'message': "El no. de lugares no puede ser un valor negativo.\n\
El no. de lugares se ha actualizado para cubrir el no. de asientos necesarios.\n\
Asientos Faltantes: %s" % abs(number_of_seats_free),
                            },
                        }
    # def write(self, vals):

    # def create(self, vals):

    # def unlink(self):

    # def search(self):


    #### herencia de funciones #####
    @api.model
    def create(self, vals):
        print ("### CREATE >>>>>>> ")
        print ("### vals ", vals)
        ### codigo antes ###
        ### self.env[''] -> Llamada a un modelo
        vals['folio'] = self.env['ir.sequence'].next_by_code('open_academy.session') or 'Nuevo'

        res = super(Session, self).create(vals)
        print ("### res ", res)
        ### codigo despues ####
        return res


    def copy(self):
        ### codigo antes ###
        self.no_copia = self.no_copia + 1
        print ("### self.no_copia", self.no_copia)
        print ("### self.name", self.name)
        res = super().copy({'name':self.name+" (copia %s)" % self.no_copia})
        ### codigo despues ####
        return res
