# -*- coding: utf-8 -*-

from odoo import models, fields # Mandatory
import platform,psutil,requests


class Ticket(models.Model):
    _name = 'gawean.ticket' # name_of_module.name_of_class 
    _description = 'Ticket Gawean' # Some note of table

    # Header
    name = fields.Char()
    tes = fields.Char()

    # Fungsi untuk mengirim pesan ke Telegram
    def send_telegram_message(bot_token, chat_id, text):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            print("Pesan telah dikirim ke Telegram.")
        else:
            print("Gagal mengirim pesan ke Telegram.")

    bot_token = '6304039480:AAHxyNNvJTYcAj9q33yHenOcqxq7eHIfp1w'
    chat_id = '6359202222'


    # Cek prosesor
    print("Platform processor     :", platform.processor())

    # Cek sistem yang digunakan
    print('System yang digunakan  :', platform.system())

    # Cek informasi disk
    disk_usage = psutil.disk_usage("/")
    print('DISK total (GB)        :', disk_usage.total / 1e9)
    print('DISK used (GB)         :', disk_usage.used / 1e9) 
    print('DISK used %            :', disk_usage.percent, "%")

    # Cek informasi RAM
    ram_info = psutil.virtual_memory()
    print('RAM total (GB)         :', ram_info.total  / 1e9)
    print('RAM Used (GB)          :', ram_info.used / 1e9) 
    print('RAM used %             :', ram_info.percent, "%")


    # Cek jika penggunaan RAM lebih besar dari atau sama dengan 50%
    if ram_info.percent >= 50:
        message = "Peringatan: Penggunaan RAM melebihi 50%! " \
                  "RAM saat ini: {}%".format(ram_info.percent)
        send_telegram_message(bot_token, chat_id, message)

    else:
        message = "pengunaan ram masih stabil" \
                  "RAM saat ini: {}%".format(ram_info.percent)
        send_telegram_message(bot_token, chat_id, message)