import requests
import os
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.header import Header

# 1. КОНФИГУРАЦИЯ (Из Secrets GitHub)
GIST_ID = os.getenv("GIST_ID")
GH_TOKEN = os.getenv("GH_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SMTP_USER = os.getenv("SMTP_USER")      
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") 

# ПОЛУЧАТЕЛЬ (Твой адрес)
EMAIL_TO = "corbih.msc@mail.ru"

# НОВЫЙ ИСТОЧНИК (BLACK VLESS)
SOURCE_URL = "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt"
DISPLAY_NAME = "🏳️MSC VPN🗽WHITE LIST⚪"

def main():
    try:
        # ШАГ 1: Загрузка ключей
        print(f"Загрузка из {SOURCE_URL}...")
        resp = requests.get(SOURCE_URL, timeout=30)
        resp.raise_for_status()
        
        # ШАГ 2: Обработка контента
        # Добавляем заголовок профиля и тег к каждому ключу
        modified_content = [f"#profile-title: {DISPLAY_NAME}"]
        for line in resp.text.splitlines():
            line = line.strip()
            if line:
                # Отсекаем старые названия после # и ставим наше
                base_link = line.split('#')[0]
                modified_content.append(f"{base_link}#MSC%20VPN")
        
        final_text = "\n".join(modified_content)

        # ШАГ 3: Обновление Gist
        print("Обновление Gist...")
        headers = {"Authorization": f"token {GH_TOKEN}"}
        gist_data = {"files": {"msc_vpn.txt": {"content": final_text}}}
        requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=gist_data).raise_for_status()

        # ШАГ 4: Формирование уведомления
        raw_url = f"https://gist.githubusercontent.com/raw/{GIST_ID}/msc_vpn.txt"
        encoded_name = urllib.parse.quote(DISPLAY_NAME)
        final_url = f"{raw_url}#{encoded_name}"
        
        msg_text = (
            f"✅ {DISPLAY_NAME} обновлен!\n\n"
            f"Новый источник: BLACK VLESS\n"
            f"Ссылка для приложения:\n{final_url}"
        )

        # ШАГ 5: Отправка в Telegram
        print("Отправка в Telegram...")
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": msg_text})
        
        # ШАГ 6: Отправка на почту (corbih.msc@mail.ru)
        print(f"Отправка на почту {EMAIL_TO}...")
        email_msg = MIMEText(msg_text, 'plain', 'utf-8')
        email_msg['Subject'] = Header(f"VPN Update: {DISPLAY_NAME}", 'utf-8')
        email_msg['From'] = SMTP_USER
        email_msg['To'] = EMAIL_TO

        with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [EMAIL_TO], email_msg.as_string())
        
        print("Успешно выполнено!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# ПРОВЕРКА ЗАПУСКА (ОБЯЗАТЕЛЬНО __name__)
if __name__ == "__main__":
    main()
