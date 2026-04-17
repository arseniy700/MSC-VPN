import requests

# Источник данных
SOURCE_URL = "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt"

# Твои настройки оформления
SUB_NAME = "🆓Free MSC VPN🗽"
SUPPORT_BOT = "https://t.me/msc_vpn_support_bot"
CHANNEL_URL = "https://t.me/MRV_S_C"

def transform_configs():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        
        # 1. Формируем "шапку" как на фото
        header = [
            f"#profile-title: {SUB_NAME}",
            "#profile-update-interval: 6",
            "#announce: 🚀 Нажми на спидометр или молнию, чтобы проверить соединение.",
            f"#support-url: {SUPPORT_BOT}",
            f"#profile-web-page-url: {CHANNEL_URL}",
            "" # Пустая строка перед ключами
        ]
        
        processed_lines = header.copy()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # 2. Обработка названий серверов
            if "#" in line:
                config_part, old_remark = line.split("#", 1)
                # Оставляем оригинальное название в скобках, добавляя твой префикс
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
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("Файл subscription.txt успешно обновлен с мета-данными!")
        
