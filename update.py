import requests

SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"
SUB_NAME = "🆓Free MSC VPN🗽"

def transform():
    try:
        headers = {'User-Agent': 'v2rayNG/1.8.5'}
        r = requests.get(SOURCE_URL, headers=headers)
        lines = r.text.splitlines()
        new_lines = []
        for line in lines:
            if line.strip() and not line.startswith("#"):
                # Просто добавляем название к каждому ключу
                if "#" in line:
                    core, name = line.rsplit("#", 1)
                    new_lines.append(f"{core}#{SUB_NAME} ({name})")
                else:
                    new_lines.append(f"{line}#{SUB_NAME}")
        return "\n".join(new_lines)
    except: return None

res = transform()
if res:
    with open("subscription.txt", "w", encoding="utf-8") as f:
        f.write(res)
        
