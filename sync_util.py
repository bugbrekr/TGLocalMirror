import pyrogram
import struct
import base64
import toml
from pymongo import MongoClient, UpdateOne
import pymongo
import uvloop
import time
import constructors
import destructors
import tqdm
from functions import _peer_to_db_name, _db_name_to_peer

uvloop.install()

mongoclient = MongoClient()
tglm_data = mongoclient["tglm_data"]
tglm_msgpool = mongoclient["tglm_messagepool"]

TQDM_ENABLE = True

def _parse_session_data(session_string):
    return struct.unpack(
        pyrogram.storage.storage.Storage.SESSION_STRING_FORMAT,
        base64.urlsafe_b64decode(session_string+"==")
    )

with open("config.toml") as f:
    config = toml.loads(f.read())

API_ID = config["telegram"]["API_ID"]
API_HASH = config["telegram"]["API_HASH"]
MAX_CONCURRENT_DOWNLOADS = config["telegram"]["MAX_CONCURRENT_DOWNLOADS"]
DEVICE_MODEL = config["tglocalgateway"]["DEVICE_MODEL"]
APP_VERSION = config["tglocalgateway"]["APP_VERSION"]

with open("db/takeout_session.dat") as f:
    session_data = f.read()

user_id = _parse_session_data(session_data)

c = pyrogram.Client(
    user_id,
    session_string=session_data,
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True,
    hide_password=True,
    device_model=DEVICE_MODEL,
    app_version=APP_VERSION,
    max_concurrent_transmissions=MAX_CONCURRENT_DOWNLOADS,
    takeout=False
)

c.start()

def initiate_takeout_session():
    return c.invoke(pyrogram.raw.functions.account.InitTakeoutSession(
            contacts=True,
            message_users=False,
            message_chats=False,
            message_megagroups=False,
            message_channels=False,
            files=False,
            file_max_size=0
        )
    ).id

def pre_populate_contact_users(takeout_id):
    contacts_raw = c.invoke(pyrogram.raw.functions.InvokeWithTakeout(takeout_id=takeout_id, query=
            pyrogram.raw.functions.contacts.GetContacts(hash=0)
    ))
    users = [destructors.User(user) for user in contacts_raw.users]
    try:
        tglm_data.validate_collection("users")
    except pymongo.errors.OperationFailure:
        tglm_data.users.create_index([('id', pymongo.ASCENDING)], name='id', unique=True)
    tglm_data.users.bulk_write([UpdateOne({"id": user["id"]}, {"$set": user}, upsert=True) for user in users])
    return len(contacts_raw.users)

def populate_dialogs_list(takeout_id):
    dialogs_raw = []
    total_chats = 1 # init value
    offset_peer = pyrogram.raw.types.InputPeerEmpty()
    offset_id = 0
    offset_date = int(time.time())
    messages = {}
    users_raw = []
    chats_raw = []
    while len(dialogs_raw) < total_chats:
        _dialogs_raw = c.invoke(pyrogram.raw.functions.InvokeWithTakeout(takeout_id=takeout_id, query=
                pyrogram.raw.functions.messages.GetDialogs(
                    offset_date=offset_date,
                    offset_id=offset_id,
                    offset_peer=offset_peer,
                    limit=100,
                    hash=0
                )
        ))
        total_chats = _dialogs_raw.count
        dialogs_raw.extend(_dialogs_raw.dialogs)
        last_peer_top_message = [msg for msg in _dialogs_raw.messages if msg.peer_id==_dialogs_raw.dialogs[-1].peer][0]
        offset_date = last_peer_top_message.date
        messages.update({pyrogram.utils.get_peer_id(msg.peer_id):msg for msg in _dialogs_raw.messages})
        users_raw.extend(_dialogs_raw.users)
        chats_raw.extend(_dialogs_raw.chats)
    dialogs = [destructors.Dialog(dialog, messages[pyrogram.utils.get_peer_id(dialog.peer)]) for dialog in dialogs_raw]
    try:
        tglm_data.validate_collection("dialogs")
    except pymongo.errors.OperationFailure:
        tglm_data.dialogs.create_index([('top_message.date', pymongo.DESCENDING)], name='date', unique=False)
    tglm_data.dialogs.bulk_write([UpdateOne({"peer": dialog["peer"]}, {"$set": dialog}, upsert=True) for dialog in dialogs])
    users = [destructors.User(user) for user in users_raw]
    try:
        tglm_data.validate_collection("users")
    except pymongo.errors.OperationFailure:
        tglm_data.users.create_index([('id', pymongo.ASCENDING)], name='id', unique=True)
    tglm_data.users.bulk_write([UpdateOne({"id": user["id"]}, {"$set": user}, upsert=True) for user in users])
    chats = [destructors.Chat(chat) for chat in chats_raw]
    try:
        tglm_data.validate_collection("chats")
    except pymongo.errors.OperationFailure:
        tglm_data.chats.create_index([('id', pymongo.ASCENDING)], name='id', unique=True)
    tglm_data.chats.bulk_write([UpdateOne({"id": chat["id"]}, {"$set": chat}, upsert=True) for chat in chats])
    return len(dialogs_raw)

def save_history_of_dialog(takeout_id, peer, resume=False, offset_id=-1):
    add_offset = 0
    _peer = constructors.InputPeer(peer)
    pbar = tqdm.tqdm(total=100, position=1, leave=False, disable=not TQDM_ENABLE)
    msgpool = tglm_msgpool[_peer_to_db_name(peer)]
    msgcounter = 0
    offset_date = int(time.time())
    try:
        tglm_msgpool.validate_collection(_peer_to_db_name(peer))
        if resume:
            last_msgs = list(msgpool.find({}, {"id": 1, "_id":0}).sort({"id":1}).limit(1))
            if len(last_msgs) == 1:
                offset_id = last_msgs[0]["id"]
        msgcounter = msgpool.count_documents({})
    except pymongo.errors.OperationFailure:
        msgpool.create_index([('id', pymongo.DESCENDING)], name='id', unique=True)
    if offset_id != -1:
        add_offset = -1
    while True:
        msgs = c.invoke(pyrogram.raw.functions.InvokeWithTakeout(takeout_id=takeout_id, query=
                pyrogram.raw.functions.messages.GetHistory(
                    peer=_peer,
                    offset_id=offset_id,
                    offset_date=offset_date,
                    add_offset=add_offset,
                    limit=100,
                    max_id=-1,
                    min_id=-1,
                    hash=0
                )
        ))
        _messages = [destructors.Message(msg) for msg in msgs.messages]
        if len(_messages) == 0:
            # if first time caching, then reaches end of list OR if second time caching with resume=False, and runs into the end of a deleted chat
            break
        if msgpool.count_documents({"id": _messages[-1]["id"]}) == 1:
            operations = [UpdateOne({"id": msg["id"]}, {"$set": msg}, upsert=True) for msg in _messages]
            msgpool.bulk_write(operations)
            # if not first time caching, and have caught up with existing list
            break
        operations = [UpdateOne({"id": msg["id"]}, {"$set": msg}, upsert=True) for msg in _messages]
        msgcounter = msgpool.count_documents({})
        if operations: msgpool.bulk_write(operations)
        pbar.total = msgs.count if not isinstance(msgs, pyrogram.raw.types.messages.Messages) else len(msgs.messages)
        pbar.refresh()
        pbar.update(msgcounter-pbar.n)
        add_offset += len(msgs.messages)
    pbar.close()
    return msgs.count if not isinstance(msgs, pyrogram.raw.types.messages.Messages) else len(msgs.messages)

def save_history_of_all_cached_dialogs(takeout_id):
    for dialog in (pbar := tqdm.tqdm(list(tglm_data.dialogs.find({})), position=0, total=tglm_data.dialogs.count_documents({}), disable=not TQDM_ENABLE)):
        peer = dialog["peer"]
        match peer["_"]:
            case "peer.user":
                peer["access_hash"] = list(tglm_data.users.find({"id": peer["user_id"]}))[0]["access_hash"]
            case "peer.channel":
                peer["access_hash"] = list(tglm_data.chats.find({"id": peer["channel_id"]}))[0]["access_hash"]
        save_history_of_dialog(takeout_id, peer, offset_id=dialog["top_message"]["id"])

if __name__=="__main__":
    print("initiating sync...")
    takeout_id = initiate_takeout_session()
    print("populating users...")
    pre_populate_contact_users(takeout_id)
    print("populating dialogs...")
    populate_dialogs_list(takeout_id)
    print("fetching messages...")
    save_history_of_all_cached_dialogs(takeout_id)
    print("done.")
