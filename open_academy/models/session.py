# -*- coding: utf-8 -*-

# Clases Base para Odoo

from odoo import models, fields, api

class SessionTag(models.Model):
    _name = "open_academy.session.tag"
    _description = 'Etiquetas de Sesiones'

    name = fields.Char('Nombre', size=64)

class Session(models.Model):
    _name = "open_academy.session"
    _description = 'Sesiones del Curso'
    
    def _current_datetime(self):
        return fields.Datetime.now()

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

    #### Query Consulta de Union de Tablas ####
    """ 
        select oas.name, rp.name nombre_sesion from open_academy_session as oas
                                   join sessions_attendances_rel as sar
                                     on sar.session_id = oas.id
                                   join res_partner as rp
                                     on rp.id = sar.partner_id
    """