from odoo import models, fields, api # 

class Ownership(models.Model):
    _name = 'domain.ownership'
    _description = 'Config ownership' 
    _check_company_auto = True

    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self : self.env.company.id)

    name = fields.Char()