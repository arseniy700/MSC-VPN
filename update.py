import requests

# Источник
SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"

# Твои настройки
SUB_NAME = "🆓Free MSC VPN🗽"
SUPPORT_BOT = "https://t.me/msc_vpn_support_bot"
CHANNEL_URL = "https://t.me/MRV_S_C"

def transform_configs():
    try:
        # Пытаемся скачать данные
        headers = {'User-Agent': 'v2rayNG/1.8.5'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Очищаем текст от лишних пробелов
        content = response.text.strip()
        if not content:
            print("Источник пуст!")
            return None
            
        lines = content.splitlines()
        
        # Шапка
        header = [
            f"#profile-title: {SUB_NAME}",
            "#profile-update-interval: 6",
            "#announce: 🚀 Нажми на спидометр или молнию, чтобы проверить соединение.",
            f"#support-url: {SUPPORT_BOT}",
            f"#profile-web-page-url: {CHANNEL_URL}",
            "" 
        ]
        
        processed_lines = header.copy()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Обработка названий
            if "#" in line:
                config_part, old_remark = line.rsplit("#", 1)
                new_line = f"{config_part}#{SUB_NAME} ({old_remark})"
            else:
                new_line = f"{line}#{SUB_NAME}"
            
            processed_lines.append(new_line)

        return "\n".join(processed_lines)

    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    result = transform_configs()
    if result:
        # Сохраняем в UTF-8 без лишних символов
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("Файл успешно создан!")
        
