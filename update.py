import requests
import base64

SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"
SUB_NAME = "🆓Free MSC VPN🗽"

def transform_configs():
    try:
        headers = {'User-Agent': 'v2rayNG/1.8.5'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=15)
        
        # Декодируем Base64, если источник зашифрован
        try:
            content = base64.b64decode(response.text).decode('utf-8')
        except:
            content = response.text
            
        lines = content.splitlines()
        processed_lines = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Меняем название сервера на твое
            if "#" in line:
                config_part, old_name = line.rsplit("#", 1)
                new_line = f"{config_part}#{SUB_NAME} ({old_name})"
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
            
