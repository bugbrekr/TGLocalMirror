import functions
import threading
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


server.run()
print("TG session manager stopped.")
graceful_exit()