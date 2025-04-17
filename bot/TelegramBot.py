import requests
import os
import time
import threading
import tempfile
import logging

from moodle.MoodleLib import MoodleLib as Moodle
from utils.dataJsonLib import dataJSON
from bot.TelegramToMoodle import TgMoodle

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Costanti
TMP_DIR = tempfile.gettempdir()
COMMANDS = ["/start", "/login", "/getchat", "/sendmessage", "/unreadmessages", "/livechat"]
COMMANDS_LOGGED = ["/getchat", "/sendmessage", "/unreadmessages", "/livechat"]
TRIGGER_WORDS = {"sparati", "muori"}
SUICIDE_EMOJI = "🤯🔫"

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"
        self.req = requests.Session()
        self.lastUpdateID = None
        self.json_file = dataJSON("users.json")
        self.moodleTool = TgMoodle(self)

    def get_updates(self, offset=None):
        try:
            url = f"{self.url}getUpdates?"
            if offset:
                url += f"offset={offset + 1}"
            response = self.req.get(url, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Errore nella richiesta getUpdates: {e}")
            return {"result": []}

    def send_TGmessage(self, message, chat_id):
        if not message:
            return
        url = f"{self.url}sendMessage?chat_id={chat_id}&text={message}"
        try:
            self.req.get(url)
        except requests.exceptions.RequestException as e:
            logging.error(f"Errore nell'invio del messaggio: {e}")
        if message == SUICIDE_EMOJI:
            self.get_last_update()
            exit(0)

    def send_photo(self, chat_id, file, caption=""):
        url = f"{self.url}sendPhoto?chat_id={chat_id}&caption={caption}"
        files = {'photo': file}
        try:
            self.req.post(url, files=files)
        except requests.exceptions.RequestException as e:
            logging.error(f"Errore nell'invio della foto: {e}")

    def send_document(self, chat_id, file, caption=""):
        url = f"{self.url}sendDocument?chat_id={chat_id}&caption={caption}"
        files = {'document': file}
        try:
            self.req.post(url, files=files)
        except requests.exceptions.RequestException as e:
            logging.error(f"Errore nell'invio del documento: {e}")

    def get_last_update(self):
        try:
            get_result = self.get_updates(self.lastUpdateID) if self.lastUpdateID else self.get_updates()
            if "result" in get_result and len(get_result["result"]) > 0:
                last_update = get_result["result"][-1]
                self.lastUpdateID = last_update["update_id"]
                return last_update
        except Exception as e:
            logging.error(f"Errore nel parsing degli aggiornamenti: {e}")
        return None

    def echo_all(self):
        last_update = self.get_last_update()
        if last_update:
            message_data = last_update.get("message", {})
            chat_id = message_data.get("chat", {}).get("id")
            username = message_data.get("from", {}).get("first_name", "utente")
            message_text = message_data.get("text", "")

            if not chat_id:
                return  # ignorare messaggi malformati

            response = ""

            if message_text == "/start":
                if self.json_file.isNewUser(chat_id):
                    response = f"Benvenuto, {username}! 👋🏼\n/login"
                    self.json_file.saveNewUser(chat_id, username)
                else:
                    response = f"Bentornato, {username}! 😁\n"
                    moodle_user = self.moodleTool.moodle.get(str(chat_id))
                    if moodle_user and moodle_user.isLogged():
                        response += "\n".join(COMMANDS_LOGGED)
                    else:
                        response += "/login"

            elif message_text.lower() in TRIGGER_WORDS:
                response = SUICIDE_EMOJI

            elif message_text == "/help":
                response = "📚 Comandi disponibili:\n" + "\n".join(COMMANDS)

            elif "ciao" in message_text.lower():
                response = f"Ciao anche a te, {username}! 😊"

            else:
                response = self.moodleTool.moodleCommands(
                    message_text, chat_id, "\n".join(COMMANDS_LOGGED), TMP_DIR
                )

            if response:
                self.send_TGmessage(response, chat_id)
