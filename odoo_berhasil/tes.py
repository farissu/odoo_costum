import platform
import psutil
import requests
import paramiko
import io

# Fungsi untuk mengirim pesan ke Telegram
def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"  # Menggunakan mode HTML untuk pesan yang lebih terstruktur
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print("Pesan telah dikirim ke Telegram.")
    else:
        print("Gagal mengirim pesan ke Telegram.")

bot_token = '6304039480:AAHxyNNvJTYcAj9q33yHenOcqxq7eHIfp1w'
chat_id = '-626240205'

# Fungsi untuk mengambil data penyimpanan (disk) dan RAM dari server melalui SSH key
# Fungsi untuk mengambil informasi sistem dari server melalui SSH key
def get_server_info_ssh(hostname, port, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname, port=port, username=username, password=password)

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
        if ram_percent >= 80 and disk_percent >=80:
            message = f"{name_Server}\n" \
                    f"\n"\
                    f"PERINGATAN RAM LEBIH DARI 80% !!!\n"\
                    f"PERINGATAN DISK LEBIH DARI 80% !!!\n"\
                    f"\n"\
                    f"RAM total (GB): {total_ram:.2f}\n" \
                    f"RAM used (GB): {used_ram:.2f}\n" \
                    f"RAM percent : {ram_percent:.2f} %\n" \
                    f"cc @Krisna"\
                    f"\n"\
                    f"DISK total (GB): {total_disk:.2f} \n" \
                    f"DISK used (GB): {used_disk:.2f}\n" \
                    f"DISK percent : {disk_percent:.2f} % \n"\
                    f"cc @Krisna"\
            
            send_telegram_message(bot_token, chat_id, message)       

        elif ram_percent >= 80 and disk_percent <=80:
            message = f"{name_Server}\n" \
                    f"\n"\
                    f"PERINGATAN RAM LEBIH DARI 80% !!!\n"\
                    f"\n"\
                    f"RAM total (GB): {total_ram:.2f}\n" \
                    f"RAM used (GB): {used_ram:.2f}\n" \
                    f"RAM percent : {ram_percent:.2f} %\n" \
                    f"cc @Krisna"\
                    f"\n"\
                    f"DISK total (GB): {total_disk:.2f} \n" \
                    f"DISK used (GB): {used_disk:.2f}\n" \
                    f"DISK percent : {disk_percent:.2f} % \n" 
            send_telegram_message(bot_token, chat_id, message)

        elif ram_percent <= 80 and disk_percent >=80:
            message = f"{name_Server}\n" \
                    f"\n"\
                    f"PERINGATAN DISK LEBIH DARI 80% !!!\n"\
                    f"\n"\
                    f"RAM total (GB): {total_ram:.2f}\n" \
                    f"RAM used (GB): {used_ram:.2f}\n" \
                    f"RAM percent : {ram_percent:.2f} %\n" \
                    f"\n"\
                    f"DISK total (GB): {total_disk:.2f} \n" \
                    f"DISK used (GB): {used_disk:.2f}\n" \
                    f"DISK percent : {disk_percent:.2f} % \n"\
                    f"cc @Krisna"
            
            send_telegram_message(bot_token, chat_id, message)

        else :
            message = f"{name_Server}\n" \
                    f"\n"\
                    f"RAM total (GB): {total_ram:.2f}\n" \
                    f"RAM used (GB): {used_ram:.2f}\n" \
                    f"RAM percent : {ram_percent:.2f} %\n" \
                    f"\n"\
                    f"DISK total (GB): {total_disk:.2f} \n" \
                    f"DISK used (GB): {used_disk:.2f}\n" \
                    f"DISK percent : {disk_percent:.2f} % \n" \

            # Kirim pesan ke Telegram
            send_telegram_message(bot_token, chat_id, message)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh_client.close()

if __name__ == "__main__":
    # Ganti dengan informasi koneksi SSH ke server Anda
    hostname = "farissu"
    name_Server = "farissu AG"
    username = "farissu"
    port = 22
    password = "farissu"

    get_server_info_ssh(hostname, port, username, password)
