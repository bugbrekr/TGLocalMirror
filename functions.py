import threading
import traceback
import socket
import secrets
import struct
import msgpack
import pyrogram
import toml
import base64
import asyncio
import _thread
import uvloop

uvloop.install()

USEABLE_UPDATES = [
    "types.UpdateNewMessage",
    "types.UpdateDeleteMessages",
    "types.UpdateChatParticipants",
    "types.UpdateUserName",
    "types.UpdateUserPhone",
    "types.UpdateChannel",
    "types.UpdateChannelTooLong",
    "types.UpdateNewChannelMessage",
    "types.UpdateDeleteChannelMessages",
    "types.UpdateEditChannelMessage",
    "types.UpdateEditMessage",
    "types.UpdatePtsChanged",
    "types.UpdateDialogPinned",
    "types.UpdatePinnedDialogs",
    "types.UpdateMessagePoll",
    "types.UpdatePeerBlocked",
    "types.UpdatePinnedMessages",
    "types.UpdatePinnedChannelMessages",
    "types.UpdateChat",
    "types.UpdateUser"
]

class TelegramSessionManager:
    def __init__(self):
        with open("config.toml") as f:
            config = toml.loads(f.read())
        self.API_ID = config["telegram"]["API_ID"]
        self.API_HASH = config["telegram"]["API_HASH"]
        self.MAX_CONCURRENT_DOWNLOADS = config["telegram"]["MAX_CONCURRENT_DOWNLOADS"]
        self.DEVICE_MODEL = config["tglocalgateway"]["DEVICE_MODEL"]
        self.APP_VERSION = config["tglocalgateway"]["APP_VERSION"]
        self.active_sessions = {}
        self.session_add_queue = []
        self._restart_flag = False
        self.sync_user_id = None
    def _parse_session_data(self, session_string):
        return struct.unpack(
            pyrogram.storage.storage.Storage.SESSION_STRING_FORMAT,
            base64.urlsafe_b64decode(session_string+"==")
        )
    def _on_raw_update(self, user_id:int, c:pyrogram.Client, update:pyrogram.raw.base.Update, users:dict, chats:dict):
        if update.QUALNAME not in USEABLE_UPDATES:
            return
        print(user_id, update.QUALNAME)
        print(update)
    def _run_sessions(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for session_data in self.session_add_queue:
            user_id = self._parse_session_data(session_data)[4]
            c = pyrogram.Client(
                user_id,
                session_string=session_data,
                api_id=self.API_ID,
                api_hash=self.API_HASH,
                in_memory=True,
                hide_password=True,
                device_model=self.DEVICE_MODEL,
                app_version=self.APP_VERSION,
                max_concurrent_transmissions=self.MAX_CONCURRENT_DOWNLOADS
            )
            c.add_handler(pyrogram.handlers.RawUpdateHandler(
                lambda client, update, users, chats: 
                    self._on_raw_update(user_id, client, update, users, chats)
                ))
            c.start()
            self.active_sessions[user_id] = c
        self.session_add_queue.clear()
        try:
            while len(self.active_sessions) == 0:
                pass
        except KeyboardInterrupt:
            return
        pyrogram.idle()
    def run(self):
        while True:
            self._run_sessions()
            if self._restart_flag == False:
                self.stop_all_sessions()
                return
            self._restart_flag = False
    def restart(self):
        self._restart_flag = True
        _thread.interrupt_main()
    def stop_all_sessions(self):
        for c in self.active_sessions.values():
            c.stop()
    def initialize_session(self, session_data, restart:bool=True, sync_user:bool=True):
        user_id = self._parse_session_data(session_data)[4]
        if user_id in self.active_sessions.keys():
            return
        self.session_add_queue.append(session_data)
        if sync_user:
            self.sync_user_id = user_id
        if restart:
            self.restart()

class Server:
    def __init__(self, telegram_manager:TelegramSessionManager, socket_path:str=None):
        self.telegram_manager = telegram_manager
        if socket_path == None:
            socket_path = "/tmp/"+secrets.token_hex(16)
        self.socket_path = socket_path
        self.s_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_sock.bind(self.socket_path)
        self.s_sock.listen(0)
        self.is_client_connected = False
        self.active_client_sock = None
        self.telegram_sessions = {}
        self._stop_flag = False
    def _recvall(self, sock, n):
        data = bytearray()
        while len(data) < n:
            try:
                packet = sock.recv(n - len(data))
                if not packet:
                    return None
                data.extend(packet)
            except ConnectionResetError:
                return None
        return data
    def _recv_msg(self, sock):
        raw_msglen = self._recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self._recvall(sock, msglen)
    def _send_msg(self, sock, data):
        data = struct.pack('>I', len(data)) + data
        try:
            sock.sendall(data)
            return data
        except:
            return None
    def _send(self, sock, data):
        packed_data = msgpack.dumps(data)
        self._send_msg(sock, packed_data)
    def _recv(self, sock):
        packed_data = self._recv_msg(sock)
        if not packed_data: return None
        data = msgpack.loads(packed_data)
        return data
    def wait_for_client(self):
        try:
            self.active_client_sock, _, = self.s_sock.accept()
        except OSError as e:
            if not self._stop_flag: print(e)
        self.is_client_connected = True
    def mainloop(self):
        if not self.is_client_connected:
            raise ConnectionError("no active connection with a client")
        try:
            while self._stop_flag == False:
                data = self._recv(self.active_client_sock)
                if not data:
                    self.active_client_sock.close()
                    self.active_client_sock = None
                    self.is_client_connected = False
                    break
                resp = self.handle_request(data)
                if resp:
                    self._send(self.active_client_sock, {"status": resp[0], "data": resp[1]})
                self._send(self.active_client_sock, "echo")
        except:
                print("------------------START CRITICAL RUNTIME ERROR------------------")
                traceback.print_exc(chain=False)
                print("-------------------END CRITICAL RUNTIME ERROR-------------------")
    def _run(self):
        while self._stop_flag == False:
            self.wait_for_client()
            if self._stop_flag: return
            self.mainloop()
    def run(self):
        self.server_thread = threading.Thread(target=self._run)
        self.server_thread.start()
        self.telegram_manager.run()
    def stop(self):
        self._stop_flag = True
        if self.is_client_connected:
            self.active_client_sock.close()
            self.active_client_sock = None
            self.is_client_connected = False
        else:
            self.s_sock.shutdown(2)
        self.server_thread.join()
    def handle_request(self, data):
        try:
            if data["type"] == "login":
                user_id = self.telegram_manager.initialize_session(data["session_data"])
        except Exception:
            print("RUNTIME ERROR:")
            traceback.print_exc(chain=False)
            return False, {"type": "RuntimeError", "traceback": traceback.format_exc(chain=False)}

class Client:
    def __init__(self, socket_path):
        self.socket_path = socket_path
    def _disconnect(self):
        self.sock.close()
    def _connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)
    def _recvall(self, sock, n):
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
    def _recv_msg(self, sock):
        raw_msglen = self._recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self._recvall(sock, msglen)
    def _send_msg(self, sock, data):
        data = struct.pack('>I', len(data)) + data
        sock.sendall(data)
        return data
    def _send(self, data):
        packed_data = msgpack.dumps(data)
        self._send_msg(self.sock, packed_data)
    def _recv(self):
        packed_data = self._recv_msg(self.sock)
        if not packed_data: return None
        data = msgpack.loads(packed_data)
        return data
    def send(self, data):
        self._send(data)
        return self._recv()

def User_to_dict(user:pyrogram.raw.types.User):
    usernames = []
    for username in user.usernames:
        username.append({
                "username": username.username,
                "editable": username.editable,
                "active": username.active
            }
        )
    return {
        "id": user.id,
        "is_self": user.is_self,
        "contact": user.contact,
        "mutual_contact": user.mutual_contact,
        "deleted": user.deleted,
        "bot": user.bot,
        "bot_chat_history": user.bot_chat_history,
        "bot_nochats": user.bot_nochats,
        "bot_inline_geo": user.bot_inline_geo,
        "bot_inline_placeholder": user.bot_inline_placeholder,
        "bot_attach_menu": user.bot_attach_menu,
        "bot_can_edit": user.bot_can_edit,
        "bot_info_version": user.bot_info_version,
        "verified": user.verified,
        "restricted": user.restricted,
        "restriction_reason": user.restriction_reason,
        "min": user.min,
        "apply_min_photo": user.apply_min_photo,
        "support": user.support,
        "scam": user.scam,
        "fake": user.fake,
        "premium": user.premium,
        "access_hash": user.access_hash,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "phone": user.phone,
        "photo": {
            "photo_id": user.photo.photo_id,
            "dc_id": user.photo.dc_id,
            "has_video": user.photo.has_video,
            "stripped_thumb": user.photo.stripped_thumb
        } if user.photo else None,
        "lang_code": user.lang_code,
        "usernames": usernames
    }

def _get_peer_type(peer):
    if isinstance(peer, pyrogram.raw.types.PeerUser):
        return "user"
    if isinstance(peer, pyrogram.raw.types.PeerChat):
        return "chat"
    if isinstance(peer, pyrogram.raw.types.PeerChannel):
        return "channel"
    return None

def Message_to_dict(msg):
    if isinstance(msg, pyrogram.raw.types.Message):
        return {
            "id": msg.id,
            "chat": {
                "type": _get_peer_type(msg.peer_id),
                "id": pyrogram.utils.get_raw_peer_id(msg.peer_id)
            },
            "date": msg.date,
            "message": msg.message,
            "out": msg.out,
            "mentioned": msg.mentioned,
            "media_unread": msg.media_unread,
            "silent": msg.silent,
            "post": msg.post,
            "from_scheduled": msg.from_scheduled,
            "pinned": msg.pinned,
            "noforwards": msg.noforwards,
            "from": {
                "type": _get_peer_type(msg.from_id),
                "id": pyrogram.utils.get_raw_peer_id(msg.from_id)
            },
            "fwd_from": {
                "date": msg.fwd_from.date,
                "from": {
                    "type": _get_peer_type(msg.fwd_from.from_id),
                    "id": pyrogram.utils.get_raw_peer_id(msg.fwd_from.from_id)
                } if msg.fwd_from.from_id else None,
                "from_name": msg.fwd_from.from_name,
                "channel_post": msg.fwd_from.channel_post,
                "post_author": msg.fwd_from.post_author,
                "saved_from_peer": {
                    "type": _get_peer_type(msg.fwd_from.saved_from_peer),
                    "id": pyrogram.utils.get_raw_peer_id(msg.fwd_from.saved_from_peer)
                } if msg.fwd_from.saved_from_peer else None,
                "saved_from_msg_id": msg.fwd_from.saved_from_msg_id
            } if msg.fwd_from else None,
            "via_bot_id": msg.via_bot_id,
            "media": "MEDIA_PLACEHOLDER", # TODO
            "views": msg.views,
            "forwards": msg.forwards,
            "edit_date": msg.edit_date,
            "post_author": msg.post_author,
            "grouped_id": msg.grouped_id
        }
    if isinstance(msg, pyrogram.raw.types.MessageService):
        return {
            "id": msg.id,
            "chat": {
                "type": _get_peer_type(msg.peer_id),
                "id": pyrogram.utils.get_raw_peer_id(msg.peer_id)
            },
            "date": msg.date,
            "action": "PLACEHOLDER", # TODO
            "out": msg.out,
            "mentioned": msg.mentioned,
            "media_unread": msg.media_unread,
            "silent": msg.silent,
            "post": msg.post,
            "from": {
                "type": _get_peer_type(msg.from_id),
                "id": pyrogram.utils.get_raw_peer_id(msg.from_id)
            }
        }

def Dialog_to_dict(dialog:pyrogram.raw.types.Dialog, top_message:dict):
    peer_id = pyrogram.utils.get_raw_peer_id(dialog.peer)
    return {
        "type": _get_peer_type(dialog.peer),
        "id": peer_id,
        "top_message": top_message,
        "read_inbox_max_id": dialog.read_inbox_max_id,
        "read_outbox_max_id": dialog.read_outbox_max_id,
        "unread_count": dialog.unread_count,
        "unread_mentions_count": dialog.unread_mentions_count,
        "unread_reactions_count": dialog.unread_reactions_count,
        "pinned": dialog.pinned,
        "unread_mark": dialog.unread_mark
    }