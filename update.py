import requests
import base64
import time

# --- НАСТРОЙКИ ---
SUB_TITLE = "🏳️MSC VPN Libertad🗽" # Можно оставить старое или поменять
SUPPORT_BOT = "https://t.me/msc_vpn_support_bot"

def transform():
    try:
        # Даже если мы не выводим серверы, оставим структуру мета-данных
        v_id = int(time.time())

        # Формируем "шапку"
        final = [
            f"#profile-title: {SUB_TITLE}",
            f"#profile-update-interval: 1",
            f"#subscription-userinfo: upload=0; download=0; total=0; expire=1", # expire=1 может подсветить, что срок вышел
            f"#support-url: {SUPPORT_BOT}",
            f"#profile-web-page-url: {SUPPORT_BOT}",
            f"#version: {v_id}",
            f"#announce: ❌ СРОК ДЕЙСТВИЯ ПОДПИСКИ ИСТЁК | 🆘 Помощь: @msc_vpn_support_bot",
            "" 
        ]
        
        # Вместо цикла по серверам добавляем ОДНУ заглушку
        # Используем любой нерабочий формат, чтобы пользователь видел только название
        final.append(f"vless://expired-id@0.0.0.0:443?encryption=none&type=tcp#❗ПОДПИСКА ИСТЕКЛА")
        
        return "\n".join(final)
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    result = transform()
    if result:
        with open("subscription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("Статус изменен на: ПОДПИСКА ИСТЕКЛА")
        
