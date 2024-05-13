import sync_util

print("initiating sync...")
takeout_id = sync_util.initiate_takeout_session()

print("fetching all messages...")
sync_util.save_history_of_all_cached_dialogs(takeout_id)
print("messages fetched.")