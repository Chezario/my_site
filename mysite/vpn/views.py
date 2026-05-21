import os
import re
import subprocess
import tempfile
import qrcode

from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


# WG_INTERFACE = "wg0"
# WG_CONFIG = "/etc/wireguard/wg0.conf"
# SERVER_PUBLIC_KEY = "SERVER_PUBLIC_KEY"
# SERVER_ENDPOINT = "vpn.example.com:51820"
# CLIENT_DNS = "1.1.1.1"
# CLIENT_ALLOWED_IPS = "0.0.0.0/0"

WG_INTERFACE = "wg0"
WG_CONFIG = "/home/www/wg0.conf"
SERVER_PUBLIC_KEY = "SERVER_PUBLIC_KEY"
SERVER_ENDPOINT = "shirokov-it.shop:51820"
CLIENT_DNS = "1.1.1.1"
CLIENT_ALLOWED_IPS = "0.0.0.0/0"

def get_vpn_users(config_path=WG_CONFIG):
    users = []
    current_user = None
    current_ip = None
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "[Peer]":
                if current_user and current_ip:
                    users.append({
                        "username": current_user,
                        "ip": current_ip
                    })
                current_user = None
                current_ip = None
            elif line.startswith("#"):
                current_user = line.lstrip("#").strip()
            elif line.startswith("AllowedIPs"):
                match = re.search(r"=\s*([^,/]+)", line)
                if match:
                    current_ip = match.group(1)
        if current_user or current_ip:
            users.append({
                "username": current_user,
                "ip": current_ip
            })
    return users


def get_used_ips():
    used = []
    with open(WG_CONFIG, "r") as f:
        for line in f:
            if "AllowedIPs" in line:
                ip = line.split("=")[1].strip()
                ip = ip.split("/")[0]
                used.append(ip)
    return used

def get_next_ip(used):
    for i in range(2, 255):
        ip = f"10.10.10.{i}"
        if ip not in used:
            return ip
    raise Exception("Свободных адресов нет")

def vpn_users_page(request):

    """

    Страница управления VPN пользователями

    """
    users = get_vpn_users()
    context = {
        'users': users
    }
    return render(request, 'vpn.html', context)

@require_http_methods(["POST"])
def create_vpn_user(request):
    username = request.POST.get("username")
    if not username:
        return JsonResponse({
            "success": False,
            "error": "Не указано имя пользователя"
        })
    try:
        private_key = subprocess.check_output(
            ["wg", "genkey"]
        ).decode().strip()
        public_key = subprocess.check_output(
            ["bash", "-c", f"echo '{private_key}' | wg pubkey"]
        ).decode().strip()
        # used_ips = get_used_ips()
        used_ips = get_used_ips()
        client_ip = get_next_ip(used_ips)
        client_config = f"""

[Interface]
PrivateKey = {private_key}
Address = {client_ip}/24
DNS = {CLIENT_DNS}

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
Endpoint = {SERVER_ENDPOINT}
AllowedIPs = {CLIENT_ALLOWED_IPS}
PersistentKeepalive = 25
"""

        peer_block = f"""
# {username}
[Peer]
PublicKey = {public_key}
AllowedIPs = {client_ip}/32
"""
        with open(WG_CONFIG, "a") as f:
            f.write(peer_block)
        subprocess.run(
            ["wg", "syncconf", WG_INTERFACE, WG_CONFIG],
            check=False
        )

        user_dir = os.path.join(
            settings.MEDIA_ROOT,
            "wireguard"
        )
        os.makedirs(user_dir, exist_ok=True)
        conf_path = os.path.join(
            user_dir,
            f"{username}.conf"
        )

        with open(conf_path, "w") as f:
            f.write(client_config)
        qr = qrcode.make(client_config)
        qr_path = os.path.join(
            user_dir,
            f"{username}.png"
        )
        qr.save(qr_path)
        return JsonResponse({
            "success": True,
            "config_file": f"/media/wireguard/{username}.conf",
            "qr_file": f"/media/wireguard/{username}.png",
            "client_ip": client_ip
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })
    
# def list_vpn_users(request):
#     users = []
#     with open(WG_CONFIG, "r") as f:
#         lines = f.readlines()
#     current_name = None
#     for line in lines:
#         line = line.strip()
#         if line.startswith("# "):
#             current_name = line[2:]
#         elif line.startswith("AllowedIPs") and current_name:
#             ip = line.split("=")[1].strip()
#             users.append({
#                 "username": current_name,
#                 "ip": ip
#             })
#             current_name = None
#     return JsonResponse(users, safe=False)

@require_http_methods(["POST"])
def delete_vpn_user(request):
    username = request.POST.get("username")
    if not username:
        return JsonResponse({
            "success": False
        })
    with open(WG_CONFIG, "r") as f:
        lines = f.readlines()
    result = []
    skip = False
    for line in lines:
        if line.strip() == f"# {username}":
            skip = True
            continue
        if skip and line.strip() == "":
            skip = False
            continue
        if not skip:
            result.append(line)
    with open(WG_CONFIG, "w") as f:
        f.writelines(result)
    subprocess.run(
        ["wg", "syncconf", WG_INTERFACE, WG_CONFIG],
        check=False
    )
    return JsonResponse({
        "success": True
    })

def download_config(request, username):

    path = os.path.join(
        settings.MEDIA_ROOT,
        "wireguard",
        f"{username}.conf"
    )

    return FileResponse(
        open(path, "rb"),
        as_attachment=True,
        filename=f"{username}.conf"
    )


