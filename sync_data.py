import sync_util

print("initiating sync...")
takeout_id = sync_util.initiate_takeout_session()
print("populating users...")
sync_util.pre_populate_contact_users(takeout_id)
print("populating dialogs...")
sync_util.populate_dialogs_list(takeout_id)