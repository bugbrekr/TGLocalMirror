import pyrogram

def InputPeer(peer:dict) -> pyrogram.raw.base.InputPeer:
    match peer["_"]:
        case "peer.channel":
            return pyrogram.raw.types.InputPeerChannel(
                channel_id=peer.get("channel_id"),
                access_hash=peer.get("access_hash")
            )
        case "peer.channel_from_message":
            return pyrogram.raw.types.InputPeerChannelFromMessage(
                peer=InputPeer(peer.get("peer")),
                msg_id=peer.get("msg_id"),
                channel_id=peer.get("channel_id")
            )
        case "peer.chat":
            return pyrogram.raw.types.InputPeerChat(
                chat_id=peer.get("chat_id")
            )
        case "peer.empty":
            return pyrogram.raw.types.InputPeerEmpty()
        case "peer.self":
            return pyrogram.raw.types.InputPeerSelf()
        case "peer.user":
            return pyrogram.raw.types.InputPeerUser(
                user_id=peer.get("user_id"),
                access_hash=peer.get("access_hash")
            )
        case "peer.user_from_message":
            return pyrogram.raw.types.InputPeerUserFromMessage(
                peer=InputPeer(peer.get("peer")),
                msg_id=peer.get("msg_id"),
                user_id=peer.get("user_id")
            )