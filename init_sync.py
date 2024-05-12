import pyrogram
import struct
import base64
import toml
from typing import List
from pymongo import MongoClient
import functions
import uvloop
import time
import helpers

uvloop.install()

mongoclient = MongoClient()
tglm_data = mongoclient["tglm_data"]
tglm_msgpool = mongoclient["tglm_messagepool"]

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

with open("db/user.dat") as f:
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
    for user in contacts_raw.users:
        _user = helpers.User(user)
        tglm_data.users.update_one({"id": _user["id"]}, {"$set": _user}, upsert=True)
    return len(contacts_raw.users)

def populate_dialogs_list(takeout_id):
    dialogs_raw = []
    total_chats = 1 # init value
    offset_peer = pyrogram.raw.types.InputPeerEmpty()
    offset_id = 0
    offset_date = int(time.time())
    messages = {}
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
    for dialog in dialogs_raw:
        _dialog = helpers.Dialog(dialog, messages[pyrogram.utils.get_peer_id(dialog.peer)])
        tglm_data.dialogs.update_one({"peer": _dialog["peer"]}, {"$set": _dialog}, upsert=True)
    return len(dialogs_raw)

takeout_id = initiate_takeout_session()
print(pre_populate_contact_users(takeout_id))
print(populate_dialogs_list(takeout_id))
