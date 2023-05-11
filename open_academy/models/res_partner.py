# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    

    session_ids = fields.Many2many('open_academy.session', 
                                     'sessions_attendances_rel', 'partner_id', 'session_id', 
                                     'Sesiones Curso')


    is_student = fields.Boolean('Es un estudiante')
    