import requests
import base64
import time
import random

# --- НАСТРОЙКИ ---
SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"
SUB_TITLE = "🏳️MSC VPN🗽"
SERVER_PREFIX = "MSC"
SUPPORT_BOT = "https://t.me/msc_vpn_support_bot"

def transform():
    try:
        # 1. Добавляем случайный параметр к источнику, чтобы сам скрипт не получал старые данные
        headers = {'User-Agent': 'v2rayNG'}
        r = requests.get(f"{SOURCE_URL}?nocache={random.random()}", headers=headers, timeout=20)
        
        if r.status_code != 200:
            print(f"Ошибка источника: {r.status_code}")
            return None
            
        text = r.text.strip()
        
        # 2. Пытаемся декодировать (источник часто в Base64)
        try:
            content = base64.b64decode(text).decode('utf-8')
        except:
            content = text
            
        lines = content.splitlines()
        
        # 3. Формируем "шапку"
        # Трафик 0/0 (total=0) в Hiddify/Happ означает бесконечность
        final = [
            f"#profile-title: {SUB_TITLE}",
            f"#profile-update-interval: 1",
            f"#subscription-userinfo: upload=0; download=0; total=0; expire=0",
            f"#support-url: {SUPPORT_BOT}",
            f"#profile-web-page-url: {SUPPORT_BOT}",
            f"#last-update: {int(time.time())}", # Метка времени для сброса кэша GitHub
            f"#announce: 🏳️БЕЛЫЕ СПИСКИ🗽 | ⚠️ВАЖНО: НЕ ДЛЯ Wi-Fi С ГЛУШИЛКАМИ | 🆘Помощь в TG",
            "" 
        ]
        
        # 4. Чистим и переименовываем серверы
        for line in lines:
            line = line.strip()
            if any(line.startswith(proto) for proto in ["vless://", "ss://", "vmess://", "trojan://"]):
                # Убираем старое название после #
                if "#" in line:
                    core = line.split("#")[0]
                    # Оставляем только часть старого имени, если нужно, или просто ставим свое
                    final.append(f"{core}#{SERVER_PREFIX} {random.randint(100,999)}") 
                else:
                    final.append(f"{line}#{SERVER_PREFIX}")
        
        return "\n".join(final)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return None

if __name__ == "__main__":
    result = transform()
    if result:
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("Файл успешно обновлен!")
        
