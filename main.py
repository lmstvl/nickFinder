from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.errors import UsernameOccupiedError, UsernameInvalidError
import time

api_id = 1  # <-- свой API ID
api_hash = ''  # <-- свой API HASH
session_name = 'my_session'  # Имя файла сессии

USERNAME_FILE = 'usernames.txt'  # Файл, откуда берём ники
DELAY = 1.2  # Задержка между попытками

def load_usernames_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]  # Удалена проверка на длину

with TelegramClient(session_name, api_id, api_hash) as client:
    me = client.get_me()
    current_username = me.username

    usernames = load_usernames_from_file(USERNAME_FILE)
    print(f"🔍 Загружено {len(usernames)} никнеймов из {USERNAME_FILE}")

    for username_to_test in usernames:
        try:
            time.sleep(DELAY)
            client(UpdateUsernameRequest(username_to_test))
            print(f"✅ Ник @{username_to_test} свободен и установлен тебе!")

            # Восстановим старый ник, если был
            if current_username:
                client(UpdateUsernameRequest(current_username))
                print(f"🔄 Вернули оригинальный ник: @{current_username}")

        except UsernameOccupiedError:
            print(f"❌ Занят: @{username_to_test}")
        except UsernameInvalidError:
            print(f"⚠️ Недопустимый формат: @{username_to_test}")
        except Exception as e:
            print(f"⚠️ Ошибка при проверке @{username_to_test}: {e}")
