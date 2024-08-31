import realtime_sync_service
import sync_util
import os
import threading
import sys

start_sync_service_flag = False

os.system(f"{sys.executable} sync_data.py")

threading.Thread(target=os.system, args=(f"{sys.executable} sync_messages.py",)).start()

print("starting sync service...")
realtime_sync_service.server.run()
print("sync service stopped.")
realtime_sync_service.graceful_exit()
