import datetime
from time import gmtime, strftime
from dateutil.relativedelta import relativedelta
import requests
from odoo.exceptions import ValidationError
from odoo import models, fields, api 


class Subdomain(models.Model):
    _name = 'domain.subdomain'
    _description = 'Domain subdomain' 
    _rec_name = 'name'
    _check_company_auto = True

    company_id = fields.Many2one(comodel_name='res.company', required=True, default=lambda self : self.env.company.id)

    name = fields.Char()
    state = fields.Char()

    @api.model
    def create(self, vals):
        today_date = datetime.datetime.now()
        if vals.get('name'):
            try :
                website_url = vals['name']
                r = requests.get(f'https://{website_url}')
                if r.status_code != 200:    
                    vals['state'] = f'DOWN'
                else:
                    vals['state'] = f'OK'
            except requests.exceptions.ConnectionError :
                raise ValidationError("Domain Not Found")

        result = super(Subdomain, self).create(vals)
        if vals['state'] == "DOWN":
            data = {
                'sub_domain_id': result.id,
                'state': result.state,
                'down': today_date,
            }
            self.env['domain.report'].create(data)
        return result
            
    def _status(self):
        website_url = self.env['domain.subdomain'].search([])
        today_date = datetime.datetime.now()
        relative_delta = relativedelta(hours=7)
        format_date = (today_date + relative_delta).strftime("%d-%m-%Y %H:%M:%S")
        for record in website_url:
            bot_info = self.env['domain.bot'].search([('aktif', '=', True)])
            r = requests.get(f'https://{record.name}')
            try:
                if r.status_code != 200:
                    record.state = str('DOWN')
                    print(r, 'r')
                    print(record.name, 'name')
                    print(record.state, 'state name')
                    message = "Domain " + str(record.name) + " " "DOWN" "\npada" " " + str(format_date) + "\nStatus Code" " " + str(r.status_code) + "&disable_web_page_preview=true"
                    url = "https://api.telegram.org/bot" + str(bot_info.botID) +"/sendMessage?text=" + str(message) + "&chat_id=" + str(bot_info.chatID)
                    requests.get(url)
                    report = self.env['domain.report'].search([('sub_domain_id','=',record.id)],order="id desc",limit=1)
                    for datas in report:
                        if datas.start:
                            print('masuk yes')
                            try:
                                data = {
                                    'sub_domain_id': record.id,
                                    'state': record.state,
                                    'down': today_date,
                                }
                                self.env['domain.report'].create(data)
                            except:
                                pass
                        else:
                            pass
                    if not report.down:
                        print('masuk not')
                        try:
                            data = {
                                'sub_domain_id': record.id,
                                'state': record.state,
                                'down': today_date,
                            }
                            self.env['domain.report'].create(data)
                        except:
                            pass
                else:
                    record.state = str('OK')
                    domain = self.env['domain.report'].search([('sub_domain_id', '=', record.id)], order="id desc", limit=1)
                    print("masuk, write_domain_up")
                    if domain:
                        print(domain, "domain")
                        for datas in domain:
                            bot_info = self.env['domain.bot'].search([('aktif', '=', True)])
                            if not datas.start :
                                r = requests.get(f'https://{record.name}')
                                datas.write({'start' : today_date})
                                if datas.start :
                                    message = "Domain " + str(record.name) + " " "UP" "\npada" " " + str(format_date) + "\nStatus Code" " " + str(r.status_code) + "\nWaktu down" " " + str(datas.time_down) + "&disable_web_page_preview=true"
                                    url = "https://api.telegram.org/bot" + str(bot_info.botID) +"/sendMessage?text=" + str(message) + "&chat_id=" + str(bot_info.chatID)
                                    requests.get(url)
                    
            except requests.exceptions.SSLError :
                message = "Domain " + str(record.name) + " " "SSL ERROR" "\npada" " " + "&disable_web_page_preview=true"
                url = "https://api.telegram.org/bot" + str(bot_info.botID) +"/sendMessage?text=" + str(message) + "&chat_id=" + str(bot_info.chatID)
                requests.get(url)
                
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
 
    # def write_domain_down(self):
    #     record = self.env['domain.subdomain'].search([('state','=','DOWN')])
    #     today_date = datetime.datetime.now()
    #     for rec in record:
    #         report = self.env['domain.report'].search([('sub_domain_id','=',rec.id)],order="id desc",limit=1)
    #         for datas in report:
    #             if datas.start:
    #                 print('masuk yes')
    #                 try:
    #                     data = {
    #                         'sub_domain_id': record.id,
    #                         'state': record.state,
    #                         'down': today_date,
    #                     }
    #                     self.env['domain.report'].create(data)
    #                 except:
    #                     pass
    #             else:
    #                 pass
    #         if not report.down:
    #             print('masuk not')
    #             try:
    #                 data = {
    #                     'sub_domain_id': record.id,
    #                     'state': record.state,
    #                     'down': today_date,
    #                 }
    #                 self.env['domain.report'].create(data)
    #             except:
    #                 pass
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }

    # def write_domain_up(self):
    #     records = self.env['domain.subdomain'].search([('state','=','OK')])
    #     today_date = datetime.datetime.now()
    #     relative_delta = relativedelta(hours=7)
    #     format_date = (today_date + relative_delta).strftime("%d-%m-%Y, %H:%M:%S")
    #     for record in records:
    #         domain = self.env['domain.report'].search([('sub_domain_id', '=', record.id)], order="id desc", limit=1)
    #         print("masuk, write_domain_up")
    #         if domain:
    #             print(domain, "domain")
    #             for datas in domain:
    #                 bot_info = self.env['domain.bot'].search([('aktif', '=', True)])
    #                 if not datas.start :
    #                     r = requests.get(f'https://{record.name}')
    #                     datas.write({'start' : today_date})
    #                     if datas.start :
    #                         message = "Domain " + str(record.name) + " " "UP" "\npada" " " + str(format_date) + "\nStatus Code" " " + str(r.status_code) + "\nWaktu down" " " + str(datas.time_down) + "&disable_web_page_preview=true"
    #                         url = "https://api.telegram.org/bot" + str(bot_info.botID) +"/sendMessage?text=" + str(message) + "&chat_id=" + str(bot_info.chatID)
    #                         requests.get(url)
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'reload',
    #         }