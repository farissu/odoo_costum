# -*- coding: utf-8 -*-

from odoo import models, fields  # Mandatory
import paramiko, psutil, requests, platform


class Ticket(models.Model):
    _name = 'gawean.server'  # name_of_module.name_of_class
    _description = 'server'  # Some note of table

    # Header
    name_server = fields.Char()
    host_name = fields.Char()
    username = fields.Char()
    port = fields.Char()
    password = fields.Char()
    sc = fields.Char()

    bot_token =  '6304039480:AAHxyNNvJTYcAj9q33yHenOcqxq7eHIfp1w'
    chat_id = '6359202222'

    # Fungsi untuk mengirim pesan ke Telegram
    def send_telegram_message(self, text=None):  # Provide a default value for 'text'
 # Use a default message if 'text' is not providedrint
        print(text)
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"  # Menggunakan mode HTML untuk pesan yang lebih terstruktur
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            print("Pesan telah dikirim ke Telegram.")
        else:
            print("Gagal mengirim pesan ke Telegram.")

    def get_server_info_ssh(self):
        data = self.env[self._name].search([])
        for record in data:
            try:
                print("masuk", record.username)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(record.host_name, port=record.port, username=record.username, password=record.password)

                # Eksekusi perintah untuk mendapatkan informasi CPU
                command_cpu = "uname -p"
                stdin, stdout, stderr = ssh_client.exec_command(command_cpu)
                platform_processor = stdout.read().decode().strip()

                # Eksekusi perintah untuk mendapatkan informasi sistem
                command_system = "uname -a"
                stdin, stdout, stderr = ssh_client.exec_command(command_system)
                system_info = stdout.read().decode().strip()

                # Eksekusi perintah untuk mendapatkan informasi RAM
                command_ram = "cat /proc/meminfo | grep MemTotal"
                stdin, stdout, stderr = ssh_client.exec_command(command_ram)
                ram_info = stdout.read().decode().strip().split(":")[1].strip()
                ram_value, ram_unit = ram_info.split()[0], ram_info.split()[1]

                if ram_unit == "kB":
                    total_ram = float(ram_value) / 1e6  # Mengubah ke GB
                elif ram_unit == "MB":
                    total_ram = float(ram_value) / 1e3  # Mengubah ke GB
                elif ram_unit == "GB":
                    total_ram = float(ram_value)
                else:
                    total_ram = float(ram_value) / 1e9  # Mengubah ke GB

                # Eksekusi perintah untuk mendapatkan informasi RAM yang digunakan
                command_used_ram = "cat /proc/meminfo | grep MemAvailable"
                stdin, stdout, stderr = ssh_client.exec_command(command_used_ram)
                used_ram_info = stdout.read().decode().strip().split(":")[1].strip()
                used_ram_value, used_ram_unit = used_ram_info.split()[0], used_ram_info.split()[1]

                if used_ram_unit == "kB":
                    used_ram = float(used_ram_value) / 1e6  # Mengubah ke GB
                elif used_ram_unit == "MB":
                    used_ram = float(used_ram_value) / 1e3  # Mengubah ke GB
                elif used_ram_unit == "GB":
                    used_ram = float(used_ram_value)
                else:
                    used_ram = float(used_ram_value) / 1e9  # Mengubah ke GB

                ram_percent = (used_ram / total_ram) * 100

                # Eksekusi perintah untuk mendapatkan informasi Disk
                command_disk = "df -h /"
                stdin, stdout, stderr = ssh_client.exec_command(command_disk)
                disk_info = stdout.read().decode().strip().split("\n")[1].split()
                total_disk_value, total_disk_unit = disk_info[1], disk_info[1][-1]
                used_disk_value, used_disk_unit = disk_info[2], disk_info[2][-1]

                if total_disk_unit == 'T':
                    total_disk = float(total_disk_value[:-1]) * 1e3
                elif total_disk_unit == 'G':
                    total_disk = float(total_disk_value[:-1])
                else:
                    total_disk = float(total_disk_value) / 1e3

                if used_disk_unit == 'T':
                    used_disk = float(used_disk_value[:-1]) * 1e3
                elif used_disk_unit == 'G':
                    used_disk = float(used_disk_value[:-1])
                else:
                    used_disk = float(used_disk_value) / 1e3

                disk_percent = (used_disk / total_disk) * 100

                # ... kode lanjutan untuk pengolahan informasi disk dan pengiriman pesan Telegram ...

                # Susun pesan untuk dikirim ke Telegram
                text = f"{record.name_server}\n" \
                    f"Platform processor: {platform_processor}\n" \
                    f"System yang digunakan: {system_info}\n" \
                    f"\n" \
                    f"RAM total (GB): {total_ram:.2f}\n" \
                    f"RAM used (GB): {used_ram:.2f}\n" \
                    f"RAM percent : {ram_percent:.2f} %\n" \
                    f"\n" \
                    f"DISK total (GB): {total_disk:.2f} \n" \
                    f"DISK used (GB): {used_disk:.2f}\n" \
                    f"DISK percent : {disk_percent:.2f} % \n"

                # Kirim pesan ke Telegram
                self.send_telegram_message(text)  # Pass the 'message' argument

            except Exception as e:
                print(f"Error: {e}")
            finally:
                ssh_client.close()
