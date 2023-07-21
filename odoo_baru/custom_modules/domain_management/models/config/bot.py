from odoo import models, fields, api


class Bot(models.Model):
    _name = 'domain.bot'
    _description = 'Config Bot' 
    _check_company_auto = True

    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self : self.env.company.id)

    name = fields.Char()
    chatID = fields.Char()
    botID = fields.Char()
    aktif = fields.Boolean()