import functions
import sys
from pymongo import MongoClient, UpdateOne
import destructors
from functions import _peer_to_db_name, _db_name_to_peer, _recursive_bytes_to_base64
import paho.mqtt.client as mqtt
import json
import threading

telegram_manager = functions.TelegramSessionManager()
mongoclient = MongoClient()
tglm_data = mongoclient["tglm_data"]
tglm_msgpool = mongoclient["tglm_messagepool"]

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = lambda a, b, c, d, e: print(a, b, c, d, e)
try:
    mqttc.connect("127.0.0.1")
except Exception as e:
    print(e)

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
    threading.Thread(target=publish_to_mqtt, args=(
        json.loads(str(update)),
        {user.id: destructors.User(user) for user in users.values()},
        {chat.id: destructors.Chat(chat) for chat in chats.values()}
    )).start()
    match update.QUALNAME:
        case "types.UpdateNewMessage":
            message = destructors.Message(update.message)
            db_peer = _peer_to_db_name(message["peer_id"])
            tglm_msgpool[db_peer].update_one({"id": message["id"]}, {"$set": message}, upsert=True)
            tglm_data.dialogs.update_one({"peer": message["peer_id"]}, {"$set": {"top_message": message}})
        case "types.UpdateNewChannelMessage":
            message = destructors.Message(update.message)
            db_peer = _peer_to_db_name(message["peer_id"])
            tglm_msgpool[db_peer].update_one({"id": message["id"]}, {"$set": message}, upsert=True)
            tglm_data.dialogs.update_one({"peer": message["peer_id"]}, {"$set": {"top_message": message}})
        case "types.UpdateDeleteMessages":
            _messages = update.messages
            deleted_msgs = []
            for chat in tglm_msgpool.list_collection_names():
                deleted_msgs.extend(list(tglm_msgpool[chat].find({"id": {"$in": _messages}})))
                instructions = [UpdateOne({"id": msg}, {"$set": {"deleted": True}}, upsert=True) for msg in _messages]
                if not instructions:
                    return
                tglm_msgpool[chat].bulk_write(instructions)
            tglm_data.deleted_messages.insert_many(deleted_msgs)
        case "types.UpdateDeleteChannelMessages":
            _messages = update.messages
            deleted_msgs = []
            chat = f"channel_{update.channel_id}"
            deleted_msgs.extend(list(tglm_msgpool[chat].find({"id": {"$in": _messages}})))
            tglm_msgpool[chat].bulk_write([UpdateOne({"id": msg}, {"$set": {"deleted": True}}, upsert=True) for msg in _messages])
            tglm_data.deleted_messages.insert_many(deleted_msgs)
        case "types.UpdateEditMessage":
            msg = destructors.Message(update.message)
            db_peer = functions._peer_to_db_name(msg["peer_id"])
            prev_msg = tglm_msgpool[db_peer].find_one({"id": msg["id"]})
            history_block = {
                "message": prev_msg["message"],
                "media": prev_msg["media"],
                "reply_markup": prev_msg["reply_markup"],
                "entities": prev_msg["entities"],
                "date": prev_msg["date"]
            }
            if isinstance(msg.get("history"), list):
                msg["history"] = prev_msg["history"].copy()
            else:
                msg["history"] = []
            msg["history"].append(history_block)
            tglm_msgpool[db_peer].update_one({"id": msg["id"]}, {"$set": msg}, upsert=True)
            tglm_data.dialogs.update_one({"peer": msg["peer_id"]}, {"$set": {"top_message": msg}})
        case "types.UpdateReadHistoryInbox":
            peer = destructors.Peer(update.peer)
            max_id = update.max_id
            still_unread_count = update.still_unread_count
            tglm_data.dialogs.update_one({"peer": peer}, {"$set": {"read_inbox_max_id": max_id, "unread_count": still_unread_count}})
        case "types.UpdateReadHistoryOutbox":
            peer = destructors.Peer(update.peer)
            max_id = update.max_id
            tglm_data.dialogs.update_one({"peer": peer}, {"$set": {"read_outbox_max_id": max_id}})
        case "types.UpdateDialogUnreadMark":
            peer = destructors.DialogPeer(update.peer).get("peer")
            if not peer: return
            tglm_data.dialogs.update_one({"peer": peer}, {"$set": {"unread_mark": update.unread}})
        case "types.UpdateUserName":
            usernames = [destructors.Username(username) for username in update.usernames]
            user_id = update.user_id
            first_name = update.first_name        
            last_name = update.last_name
            tglm_data.users.update_one({"id": user_id}, {"$set": {"first_name": first_name, "last_name": last_name, "usernames": usernames}})
        case "types.UpdateUserPhone":
            user_id = update.user_id
            phone = update.phone
            tglm_data.users.update_one({"id": user_id}, {"$set": {"phone": phone}})
        case "types.UpdateDialogPinned":
            if update.folder_id: return
            peer = destructors.DialogPeer(update.peer).get("peer")
            pinned = update.pinned
            tglm_data.dialogs.update_one({"peer": peer}, {"$set": {"pinned": pinned}})
        case "types.UpdatePinnedMessages":
            peer = destructors.Peer(update.peer)
            db_peer = functions._peer_to_db_name(peer)
            pinned = update.pinned
            if pinned==None: return
            tglm_msgpool[db_peer].bulk_write([UpdateOne({"id": msg}, {"$set": {"pinned": pinned}}, upsert=True) for msg in update.messages])
        case "types.UpdatePinnedChannelMessages":
            channel_id = update.channel_id
            db_peer = f"channel_{channel_id}"
            pinned = update.pinned
            if pinned==None: return
            tglm_msgpool[db_peer].bulk_write([UpdateOne({"id": msg}, {"$set": {"pinned": pinned}}, upsert=True) for msg in update.messages])

def publish_to_mqtt(update, users, chats):
    payload = {
            "update": _recursive_bytes_to_base64(update),
            "users": _recursive_bytes_to_base64(users),
            "chats": _recursive_bytes_to_base64(chats)
        }
    if not mqttc.is_connected():
        mqttc.reconnect()
    mqttc.publish("TGLocalMirror/update", json.dumps(payload))


if __name__=="__main__":
    server.run()
    print("TG session manager stopped.")
    graceful_exit()