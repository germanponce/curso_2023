# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.depends('session_ids')
    def _is_an_student(self):
        for rec in self:
            if rec.session_ids:
                rec.is_student = True
            else:
                rec.is_student = False

    session_ids = fields.Many2many('open_academy.session', 
                                     'sessions_attendances_rel', 'partner_id', 'session_id', 
                                     'Sesiones Curso')


    is_student = fields.Boolean('Es un estudiante', compute="_is_an_student", store=True)

