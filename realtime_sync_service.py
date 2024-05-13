import functions
import sys

telegram_manager = functions.TelegramSessionManager()

try:
    with open("db/user.dat") as f:
        user_session = f.read()
    telegram_manager.initialize_session(user_session, restart=False, sync_user=True)
except FileNotFoundError:
    pass

def graceful_exit():
    server.stop()
    print("Service stopped.")
    sys.exit(0)

server = functions.Server(telegram_manager)
with open("db/socket_path", "w") as f:
    f.write(server.socket_path)

@telegram_manager.on_raw_update()
def on_raw_update(user_id:int, c:functions.pyrogram.Client, update:functions.pyrogram.raw.base.Update, users:dict, chats:dict):
    print(update.QUALNAME)

server.run()
print("TG session manager stopped.")
graceful_exit()