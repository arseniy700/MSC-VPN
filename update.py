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
        # 1. Загрузка данных с защитой от кэша
        headers = {'User-Agent': 'v2rayNG'}
        r = requests.get(f"{SOURCE_URL}?nc={random.random()}", headers=headers, timeout=20)
        
        if r.status_code != 200:
            return None
            
        text = r.text.strip()
        
        # 2. Декодирование Base64
        try:
            content = base64.b64decode(text).decode('utf-8')
        except:
            content = text
            
        lines = content.splitlines()
        
        # 3. Шапка подписки
        final = [
            f"#profile-title: {SUB_TITLE}",
            f"#profile-update-interval: 1",
            f"#subscription-userinfo: upload=0; download=0; total=0; expire=0",
            f"#support-url: {SUPPORT_BOT}",
            f"#profile-web-page-url: {SUPPORT_BOT}",
            f"#last-update: {int(time.time())}",
            f"#announce: 🏳️БЕЛЫЕ СПИСКИ🗽 | ⚠️ВАЖНО: НЕ ДЛЯ Wi-Fi С ГЛУШИЛКАМИ | 🆘Помощь в TG",
            "" 
        ]
        
        # 4. Правильное переименование серверов
        for line in lines:
            line = line.strip()
            if any(line.startswith(proto) for proto in ["vless://", "ss://", "vmess://", "trojan://"]):
                if "#" in line:
                    # Разделяем ссылку и старое название
                    parts = line.split("#", 1)
                    config_link = parts[0]
                    old_name = parts[1]
                    
                    # Убираем лишние префиксы из старого названия, если они там есть
                    clean_name = old_name.replace("бесплатный", "").replace("free", "").strip()
                    
                    # Итоговое название: MSC Название
                    final.append(f"{config_link}#{SERVER_PREFIX} {clean_name}")
                else:
                    final.append(f"{line}#{SERVER_PREFIX}")
        
        return "\n".join(final)
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    result = transform()
    if result:
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("Файл успешно обновлен с правильными названиями!")
        
