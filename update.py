import requests

# Ссылка на оригинал
SOURCE_URL = "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt"
CUSTOM_NAME = "🆓Free MSC VPN🗽"

def transform_configs():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        processed_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Разделяем ссылку и старое название (всё, что после #)
            if "#" in line:
                config_part, old_remark = line.split("#", 1)
                # Формат: Ссылка#🆓Free MSC VPN🗽 (Оригинал)
                new_line = f"{config_part}#{CUSTOM_NAME} ({old_remark})"
            else:
                # Если названия не было, просто добавляем своё
                new_line = f"{line}#{CUSTOM_NAME}"
            
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
        print("Файл subscription.txt успешно обновлен!")
        
