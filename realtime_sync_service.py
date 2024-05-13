import functions
import sys
from pymongo import MongoClient, UpdateOne
import pymongo
import destructors
from functions import _peer_to_db_name, _db_name_to_peer

telegram_manager = functions.TelegramSessionManager()
mongoclient = MongoClient()
tglm_data = mongoclient["tglm_data"]
tglm_msgpool = mongoclient["tglm_messagepool"]

try:
    with open("db/sync_session.dat") as f:
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

def update_users(users_list):
    if len(users_list) == 0: return
    _users = [destructors.User(user) for user in users_list]
    tglm_data.users.bulk_write([UpdateOne({"id": user["id"]}, {"$set": user}, upsert=True) for user in _users])

def update_chats(chats_list):
    if len(chats_list) == 0: return
    _chats = [destructors.Chat(chat) for chat in chats_list]
    tglm_data.chats.bulk_write([UpdateOne({"id": chat["id"]}, {"$set": chat}, upsert=True) for chat in _chats])

@telegram_manager.on_raw_update
def on_raw_update(user_id:int, c:functions.pyrogram.Client, update:functions.pyrogram.raw.base.Update, users:dict, chats:dict):
    update_users(users.values())
    update_chats(chats.values())
    print(update.QUALNAME)
    match update.QUALNAME:
        case "types.UpdateNewMessage":
            message = destructors.Message(update.message)
            db_peer = _peer_to_db_name(message["peer_id"])
            tglm_msgpool[db_peer].insert_one(message)

if __name__=="__main__":
    server.run()
    print("TG session manager stopped.")
    graceful_exit()