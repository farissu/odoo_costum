import whois
import datetime
import requests
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api 

class Main(models.Model):
    _name = 'domain.main'
    _description = 'Domain Main' 
    _check_company_auto = True

    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self : self.env.company.id)

    name = fields.Char()
    registrar = fields.Char()
    creation_date = fields.Date()
    expiration_date = fields.Date()
    range_date = fields.Char(compute='_expire')
    updated_date = fields.Date()
    management = fields.Many2one(comodel_name='domain.management')
    renewal_status = fields.Selection([
        ('diperpanjang', 'Perpanjang'),
        ('akan', 'Akan di perpanjang'),
        ('tidak', 'Tidak di perpanjang'),
        ('sudah', 'Sudah di perpanjang'),
        ('New', 'New'),
    ])
    ownership = fields.Many2one(comodel_name='domain.ownership')
    domain_tld = fields.Char()
    hpp_rupiah = fields.Integer()
    hpp_usd = fields.Char()
            
    @api.model
    def create(self, vals):
        if vals.get('name'):
            try:
                w = whois.whois(vals['name'])
                vals['registrar'] = w.registrar
                if type(w.creation_date) == list:
                    vals['creation_date'] = w.creation_date[0]
                else :
                    vals['creation_date'] = w.creation_date
                if type(w.expiration_date) == list:
                    vals['expiration_date'] = w.expiration_date[0]
                else :
                    vals['expiration_date'] = w.expiration_date
                if type(w.updated_date) == list:
                    vals['updated_date'] = w.updated_date[0]
                else :
                    vals['updated_date'] = w.updated_date
            except whois.parser.PywhoisError:
                raise ValidationError("Domain Not Found")
        return super(Main, self).create(vals)
        

    def update_domain(self):
        domain = self.env['domain.main'].search([])
        today_date = datetime.date.today()
        for record in domain:
            expiration_date = fields.Datetime.to_datetime(record.expiration_date).date()
            total_waktu = int((expiration_date - today_date).days)
            if total_waktu == 30 or total_waktu == 15 or total_waktu == 10 or total_waktu <= 5:
                w = whois.whois(record.name)
                record.registrar = w.registrar
                if type(w.creation_date) == list:
                    record.creation_date = w.creation_date[0]
                else :
                    record.creation_date = w.creation_date
                if type(w.expiration_date) == list:
                    record.expiration_date = w.expiration_date[0]
                else :
                    record.expiration_date = w.expiration_date
                if type(w.updated_date) == list:
                    record.updated_date = w.updated_date[0]
                else :
                    record.updated_date = w.updated_date
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }

    def _expire(self):
        today_date = datetime.date.today()
        for waktu in self:
            if waktu.expiration_date:
                expiration_date = fields.Datetime.to_datetime(waktu.expiration_date).date()
                total_waktu = str(int((expiration_date - today_date).days))
                akumulasi = int((expiration_date - today_date).days)
                waktu.range_date = str(total_waktu + ' Hari')
                if akumulasi <= -7:
                    waktu.range_date = str('Expired')
            else :
                waktu.range_date = False
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def kirim_tele(self):
        domain = self.env['domain.main'].search([])
        today_date = datetime.date.today()
        for record in domain:
            bot_info = self.env['domain.bot'].search([('aktif', '=', True)])
            for bot in bot_info:
                expiration_date = fields.Datetime.to_datetime(record.expiration_date).date()
                total_waktu = int((expiration_date - today_date).days)
                format_date = (record.expiration_date).strftime("%d-%m-%Y")
                if bot.aktif:
                    # if total_waktu == 54:
                    if total_waktu == 30 or total_waktu == 15 or total_waktu == 10 or total_waktu <= 5 and total_waktu >= 0:
                        message = "Domain " + str(record.name) + "\nAkan Expired " + (record.range_date) + " Lagi\n" "Tanggal " + str(format_date) + "&disable_web_page_preview=true"
                        url = "https://api.telegram.org/bot" + str(bot.botID) +"/sendMessage?text=" + str(message) + "&chat_id=" + str(bot.chatID)
                        requests.get(url)
                    elif total_waktu < 0 and total_waktu > -5:
                        message = "Domain " + str(record.name) + "\nSudah Expired " + (record.range_date) + "\nTanggal " + str(format_date) + "&disable_web_page_preview=true"
                        url = "https://api.telegram.org/bot" + str(bot.botID) +"/sendMessage?text=" + str(message) + "&chat_id=" + str(bot.chatID)
                        requests.get(url)
                    elif total_waktu == -5 or total_waktu == -6:
                        message = "Domain " + str(record.name) + "\nExpired" + "&disable_web_page_preview=true"
                        url = "https://api.telegram.org/bot" + str(bot.botID) +"/sendMessage?text=" + str(message) + "&chat_id=" + str(bot.chatID)
                        requests.get(url)
                    else:
                        pass
                else:
                    pass
