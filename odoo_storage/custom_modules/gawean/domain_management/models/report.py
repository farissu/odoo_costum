import datetime
import time
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api 


class Report(models.Model):
    _name = 'domain.report'
    _description = 'Domain report'
    _rec_name = 'sub_domain_id' 
    _check_company_auto = True

    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self : self.env.company.id)

    sub_domain_id = fields.Many2one(comodel_name="domain.subdomain", string='sub_domain', ondelete='cascade')
    down = fields.Datetime()
    start = fields.Datetime()
    state = fields.Char()
    time_down = fields.Char(compute="_compute_time_down")
    
    @api.depends('start','down')
    def _compute_time_down(self):
        for record in self:
            if record.start:
                calculate = record.start - record.down
                micro = calculate - datetime.timedelta(microseconds=calculate.microseconds)
                record.time_down = str(micro)
            else:
                record.time_down = False