from bot.TelegramBot import TelegramBot
from bot_token import TELEGRAM_BOT_TOKEN
import time

def main():
    token = TELEGRAM_BOT_TOKEN
    bot = TelegramBot(token)
    print(bot.get_updates())

    while True:
        try:
            bot.echo_all()
        except Exception as e:
            print(f"Errore nel loop principale: {e}")
            time.sleep(5)  # evita loop troppo veloce in caso di crash

if __name__ == "__main__":
    main()
