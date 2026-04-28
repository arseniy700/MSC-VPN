import requests

# Новый источник данных
SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"

# Твои настройки оформления
SUB_NAME = "🆓Free MSC VPN🗽"
SUPPORT_BOT = "https://t.me/msc_vpn_support_bot"
CHANNEL_URL = "https://t.me/MRV_S_C"

def transform_configs():
    try:
        # Устанавливаем User-Agent, чтобы сервер не заблокировал запрос от бота
        headers = {'User-Agent': 'v2rayNG/1.8.5'}
        response = requests.get(SOURCE_URL, headers=headers)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        
        # Шапка профиля (мета-данные для приложений)
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
            # Пропускаем пустые строки и комментарии, которые уже могут быть в источнике
            if not line or line.startswith("#"):
                continue
            
            # Обработка названий
            if "#" in line:
                # Если в ссылке уже есть имя, берем его в скобки
                config_part, old_remark = line.rsplit("#", 1)
                new_line = f"{config_part}#{SUB_NAME} ({old_remark})"
            else:
                # Если имени нет, просто ставим свое
                new_line = f"{line}#{SUB_NAME}"
            
            processed_lines.append(new_line)

        return "\n".join(processed_lines)

    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None

if __name__ == "__main__":
    result = transform_configs()
    if result:
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("Подписка успешно обновлена из нового источника!")
        
