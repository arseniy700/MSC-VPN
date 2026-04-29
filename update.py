import requests
import base64
import time

# --- НАСТРОЙКИ ---
SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"
SUB_TITLE = "🏳️MSC VPN🗽"
SERVER_PREFIX = "MSC"
SUPPORT_BOT = "https://t.me/msc_vpn_support_bot"
# -----------------

def get_data():
    try:
        headers = {'User-Agent': 'v2rayNG'}
        r = requests.get(SOURCE_URL, headers=headers, timeout=20)
        text = r.text.strip()
        try:
            return base64.b64decode(text).decode('utf-8')
        except:
            return text
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None

def transform():
    data = get_data()
    if not data:
        return None
    
    lines = data.splitlines()
    v_id = int(time.time()) # Уникальное число для сброса кэша

    # Формируем «шапку» (интерфейс приложения)
    final = [
        f"#profile-title: {SUB_TITLE}",
        f"#profile-update-interval: 1",
        f"#subscription-userinfo: upload=0; download=0; total=0; expire=0",
        f"#support-url: {SUPPORT_BOT}",
        f"#profile-web-page-url: {SUPPORT_BOT}",
        f"#version: {v_id}",
        "#announce: 🏳️БЕЛЫЕ СПИСКИ🗽 | ⚠️ВАЖНО: НЕ ДЛЯ Wi-Fi С ГЛУШИЛКАМИ | 🆘Помощь в TG",
        "" 
    ]
    
