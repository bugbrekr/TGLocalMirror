import pyrogram

def InputPeer(peer:dict) -> pyrogram.raw.base.InputPeer:
    match peer["_"]:
        case "input_peer.channel":
            return pyrogram.raw.types.InputPeerChannel(
                channel_id=peer["channel_id"],
                access_hash=peer["access_hash"]
            )
        case "input_peer.channel_from_message":
            return pyrogram.raw.types.InputPeerChannelFromMessage(
                peer=InputPeer(peer["peer"]),
                msg_id=peer["msg_id"],
                channel_id=peer["channel_id"]
            )
        case "input_peer.chat":
            return pyrogram.raw.types.InputPeerChat(
                chat_id=peer["chat_id"]
            )
        case "input_peer.empty":
            return pyrogram.raw.types.InputPeerEmpty()
        case "input_peer.self":
            return pyrogram.raw.types.InputPeerSelf()
        case "input_peer.user":
            return pyrogram.raw.types.InputPeerUser(
                user_id=peer["user_id"],
                access_hash=peer["access_hash"]
            )
        case "input_peer.user_from_message":
            return pyrogram.raw.types.InputPeerUserFromMessage(
                peer=InputPeer(peer["peer"]),
                msg_id=peer["msg_id"],
                user_id=peer["user_id"]
            )