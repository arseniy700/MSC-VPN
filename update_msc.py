import requests
import os
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.header import Header

# Секреты (убедись, что они добавлены в Settings -> Secrets этого репозитория)
GIST_ID = os.getenv("GIST_ID")
GH_TOKEN = os.getenv("GH_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SMTP_USER = os.getenv("SMTP_USER")      
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") 

EMAIL_TO = "corbih.msc@mail.ru"
SOURCE_URL = "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt"
DISPLAY_NAME = "🏳️MSC VPN🗽WHITE LIST⚪"

def main():
    try:
        print("Скачивание ключей...")
        resp = requests.get(SOURCE_URL, timeout=30)
        resp.raise_for_status()
        
        modified = [f"#profile-title: {DISPLAY_NAME}"]
        for line in resp.text.splitlines():
            if line.strip():
                link = line.split('#')[0]
                modified.append(f"{link}#MSC%20VPN")
        
        print("Обновление Gist...")
        headers = {"Authorization": f"token {GH_TOKEN}"}
        data = {"files": {"msc_vpn.txt": {"content": "\n".join(modified)}}}
        requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=data).raise_for_status()

        raw_url = f"https://gist.githubusercontent.com/raw/{GIST_ID}/msc_vpn.txt"
        final_url = f"{raw_url}#{urllib.parse.quote(DISPLAY_NAME)}"
        msg = f"✅ {DISPLAY_NAME} обновлен!\n\nСсылка:\n{final_url}"

        # Отправка TG
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": msg})
        
        # Отправка Email
        email_msg = MIMEText(msg, 'plain', 'utf-8')
        email_msg['Subject'] = Header("MSC VPN Update", 'utf-8')
        email_msg['From'] = SMTP_USER
        email_msg['To'] = EMAIL_TO

        with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [EMAIL_TO], email_msg.as_string())
        print("Выполнено успешно!")

    except Exception as e:
        print(f"Ошибка: {e}")

# ОБЯЗАТЕЛЬНО: Двойные подчеркивания здесь!
if __name__ == "__main__":
    main()
    
