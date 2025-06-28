import os
import requests

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None

if __name__ == "__main__":
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Error: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in environment")
    else:
        current_time = "12:17 AM -05 on Saturday, June 28, 2025"  # Hora actual
        message = f"Prueba del bot a las {current_time} Lima"
        result = send_telegram_message(token, chat_id, message)
        if result:
            print("Message sent successfully:", result)
        else:
            print("Failed to send message")