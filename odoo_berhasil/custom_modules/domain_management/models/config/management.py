from odoo import models, fields, api # 


class Management(models.Model):
    _name = 'domain.management'
    _description = 'Config Management' 
    _check_company_auto = True

    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self : self.env.company.id)

    name = fields.Char()