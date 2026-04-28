import requests
import base64

SOURCE_URL = "https://sub.pfvpn.cfd/free/sub"
SUB_TITLE = "🏳️MSC VPN🗽"
SERVER_PREFIX = "MSC"

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
        # Новая шапка
        final = [f"#profile-title: {SUB_TITLE}", "#profile-update-interval: 6", ""]
        
        for line in lines:
            line = line.strip()
            if line.startswith(("vless://", "ss://", "vmess://", "trojan://")):
                if "#" in line:
                    core = line.rsplit("#", 1)[0]
                    old_name = line.rsplit("#", 1)[1]
                    final.append(f"{core}#{SERVER_PREFIX} {old_name}")
                else:
                    final.append(f"{line}#{SERVER_PREFIX}")
        return "\n".join(final)
    except:
        return None

res = transform()
if res:
    with open("subscription.txt", "w", encoding="utf-8") as f:
        f.write(res)
        
