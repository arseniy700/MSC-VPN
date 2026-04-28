import requests
import base64

SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"
SUB_TITLE = "🏳️MSC VPN🗽"
SERVER_PREFIX = "MSC"
SUPPORT_BOT = "https://t.me/msc_vpn_support_bot"

def transform():
    try:
        headers = {'User-Agent': 'v2rayNG'}
        r = requests.get(SOURCE_URL, headers=headers, timeout=20)
        text = r.text.strip()
        
        try:
            content = base64.b64decode(text).decode('utf-8')
        except:
            content = text
            
        lines = content.splitlines()

        # Новая экспериментальная шапка без сложных переносов
        final = [
            f"#profile-title: {SUB_TITLE}",
            "#profile-update-interval: 6",
            "#subscription-userinfo: upload=0; download=0; total=0; expire=0",
            f"#support-url: {SUPPORT_BOT}",
            f"#profile-web-page-url: {SUPPORT_BOT}",
            # Описание одной строкой, так оно надежнее
            "#announce: 🏳️БЕЛЫЕ СПИСКИ🗽 | ⚠️ВАЖНО: НЕ ДЛЯ Wi-Fi С ГЛУШИЛКАМИ | 🆘Помощь в TG",
            "" 
        ]
        
        server_count = 0
        for line in lines:
            line = line.strip()
            if line.startswith(("vless://", "ss://", "vmess://", "trojan://")):
                server_count += 1
                if "#" in line:
                    core = line.rsplit("#", 1)[0]
                    old_name = line.rsplit("#", 1)[1]
                    final.append(f"{core}#{SERVER_PREFIX} {old_name}")
                else:
                    final.append(f"{line}#{SERVER_PREFIX}")
        
        if server_count == 0:
            print("Серверы не найдены в источнике!")
            return None
            
        return "\n".join(final)
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

res = transform()
if res:
    with open("subscription.txt", "w", encoding="utf-8") as f:
        f.write(res)
    print("Файл успешно обновлен!")
    
