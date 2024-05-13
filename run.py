import realtime_sync_service
import sync_util
import os
import threading

start_sync_service_flag = False

os.system("python3 sync_data.py")

threading.Thread(target=os.system, args=("python3 sync_messages.py",)).start()

print("starting sync service...")
realtime_sync_service.server.run()
print("sync service stopped.")
realtime_sync_service.graceful_exit()