import requests
import base64

SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"
SUB_NAME = "🆓Free MSC VPN🗽"

def get_data():
    try:
        # Пытаемся получить данные с правильным заголовком
        r = requests.get(SOURCE_URL, headers={'User-Agent': 'v2rayNG'}, timeout=20)
        text = r.text.strip()
        
        # Если это Base64, декодируем его
        try:
            decoded = base64.b64decode(text).decode('utf-8')
            return decoded
        except:
            return text # Если это уже текст, возвращаем как есть
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None

data = get_data()
if data:
    lines = data.splitlines()
    final = []
    for line in lines:
        if line.startswith("vless://") or line.startswith("ss://") or line.startswith("vmess://"):
            # Очищаем от старых имен и ставим твое
            if "#" in line:
                core = line.split("#")[0]
                old_name = line.split("#")[1]
                final.append(f"{core}#{SUB_NAME} ({old_name})")
            else:
                final.append(f"{line}#{SUB_NAME}")
    
    with open("subscription.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final))
    print("Файл успешно перезаписан!")
    
