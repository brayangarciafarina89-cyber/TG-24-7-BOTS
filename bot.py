import os
import time
import requests

TOKEN = os.environ["8955760982:AAEYwYz4tVZkd2IxcznEXyzTM9TMzW4nb-A"]
API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=20
    ).raise_for_status()

def main():
    offset = 0
    print("Bot iniciado. Esperando mensajes...")

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 25},
                timeout=35
            )
            response.raise_for_status()

            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                text = message.get("text", "")

                if not chat or not text:
                    continue

                if text.startswith("/start"):
                    reply = (
                        "¡Hola! Soy tu bot de Telegram. "
                        "Estoy listo para ayudarte."
                    )
                else:
                    reply = f"Recibí tu mensaje: {text}"

                send_message(chat["id"], reply)

        except Exception as error:
            print(f"Error: {error}")
            time.sleep(5)

if __name__ == "__main__":
    main()
