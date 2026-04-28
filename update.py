import requests
import base64

# Источник данных
SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"

# Настройки названий
SUB_TITLE = "🏳️MSC VPN🗽" # Название всей подписки (сверху)
SERVER_PREFIX = "MSC"    # Название перед каждым сервером

def get_data():
    try:
        headers = {'User-Agent': 'v2rayNG'}
        r = requests.get(SOURCE_URL, headers=headers, timeout=20)
        text = r.text.strip()
        
        # Пробуем декодировать Base64
        try:
            return base64.b64decode(text).decode('utf-8')
        except:
            return text
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None

data = get_data()
if data:
    lines = data.splitlines()
    
    # Формируем файл
    # 1. Шапка для названия подписки сверху
    final_content = [
        f"#profile-title: {SUB_TITLE}",
        "#profile-update-interval: 6",
        "" # Пустая строка
    ]
    
    # 2. Обработка каждого сервера
    for line in lines:
        line = line.strip()
        if line.startswith(("vless://", "ss://", "vmess://", "trojan://")):
            if "#" in line:
                core, old_name = line.rsplit("#", 1)
                # Формат: MSC Название_сервера
                final_content.append(f"{core}#{SERVER_PREFIX} {old_name}")
            else:
                final_content.append(f"{line}#{SERVER_PREFIX}")
    
    # Сохраняем результат
    with open("subscription.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_content))
    print("Готово! Подписка обновлена.")
    
