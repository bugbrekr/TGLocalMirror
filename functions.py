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

class TelegramSessionManager:
    def __init__(self, api_id=None, api_hash=None):
        with open("config.toml") as f:
            config = toml.loads(f.read())
        self.API_ID = api_id if api_id else config["telegram"]["API_ID"]
        self.API_HASH = api_hash if api_hash else config["telegram"]["API_HASH"]
        self.active_sessions = {}
        self.session_add_queue = []
        self._restart_flag = False
    def _parse_session_data(self, session_string):
        return struct.unpack(
            pyrogram.storage.storage.Storage.SESSION_STRING_FORMAT,
            base64.urlsafe_b64decode(session_string+"==")
        )
    def _on_raw_update(self, user_id, c, update, users, chats):
        print(user_id, update)
        print(users)
        print(chats)
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
                device_model="TGLocalGateway",
                app_version="TGLocalGateway 1.0"
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
    def initialize_session(self, session_data):
        user_id = self._parse_session_data(session_data)[4]
        if user_id in self.active_sessions.keys():
            return
        self.session_add_queue.append(session_data)
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
    def run(self):
        while self._stop_flag == False:
            self.wait_for_client()
            if self._stop_flag: return
            self.mainloop()
    def stop(self):
        self._stop_flag = True
        if self.is_client_connected:
            self.active_client_sock.close()
            self.active_client_sock = None
            self.is_client_connected = False
        else:
            self.s_sock.shutdown(2)
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