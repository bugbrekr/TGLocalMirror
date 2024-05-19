import json
import pyrogram

def Peer(peer:pyrogram.raw.base.Peer) -> dict:
    if isinstance(peer, pyrogram.raw.types.PeerChannel):
        return {
            "_": "peer.channel",
            "channel_id": peer.channel_id
        }
    if isinstance(peer, pyrogram.raw.types.PeerChat):
        return {
            "_": "peer.chat",
            "chat_id": peer.chat_id
        }
    if isinstance(peer, pyrogram.raw.types.PeerUser):
        return {
            "_": "peer.user",
            "user_id": peer.user_id
        }

def RestrictionReason(reason:pyrogram.raw.base.RestrictionReason) -> dict:
    if isinstance(reason, pyrogram.raw.types.RestrictionReason):
        return {
            "_": "restrict_reason.restriction_reason",
            "platform": reason.platform,
            "reason": reason.reason,
            "text": reason.text
        }

def Username(username:pyrogram.raw.base.Username) -> dict:
    if isinstance(username, pyrogram.raw.types.Username):
        return {
            "_": "username.username",
            "username": username.username,
            "editable": username.editable,
            "active": username.active
        }

def User(user:pyrogram.raw.base.User) -> dict:
    if isinstance(user, pyrogram.raw.types.User):
        return {
            "_": "user.user",
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
            "restriction_reason": [RestrictionReason(reason) for reason in user.restriction_reason],
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
            "usernames": [Username(username) for username in user.usernames]
        }
    if isinstance(user, pyrogram.raw.types.UserEmpty):
        return {
            "_": "user.empty",
            "id": user.id
        }

def Chat(chat:pyrogram.raw.base.Chat) -> dict:
    return json.loads(str(chat)) if chat else None

def InputStickerSet(sticker:pyrogram.raw.base.InputStickerSet) -> dict:
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetAnimatedEmoji):
        return {
            "_": "stickerset.animated_emoji",
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetAnimatedEmojiAnimations):
        return {
            "_": "stickerset.animated_emoji_animations",
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetDice):
        return {
            "_": "stickerset.dice",
            "emoticon": sticker.emoticon
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetEmojiDefaultStatuses):
        return {
            "_": "stickerset.emoji_default_statuses"
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetEmojiDefaultTopicIcons):
        return {
            "_": "stickerset.emoji_default_topic_icons"
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetEmojiGenericAnimations):
        return {
            "_": "stickerset.emoji_generic_animations"
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetEmpty):
        return {
            "_": "stickerset.empty"
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetID):
        return {
            "_": "stickerset.id",
            "id": sticker.id,
            "access_hash": sticker.access_hash
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetPremiumGifts):
        return {
            "_": "stickerset.premium_gifts"
        }
    if isinstance(sticker, pyrogram.raw.types.InputStickerSetShortName):
        return {
            "_": "stickerset.short_name",
            "short_name": sticker.short_name
        }

def MaskCoords(coords:pyrogram.raw.base.MaskCoords) -> dict:
    if isinstance(coords, pyrogram.raw.types.MaskCoords):
        return {
                "_": "mask_coords.mask_coords",
                "n": coords.n,
                "x": coords.x,
                "y": coords.y,
                "zoom": coords.zoom
            }

def DocumentAttribute(attr:pyrogram.raw.base.DocumentAttribute) -> dict:
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeAnimated):
        return {
            "_": "document.attribute.animated"
        }
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeAudio):
        return {
            "_": "document.attribute.audio",
            "duration": attr.duration,
            "voice": attr.voice,
            "title": attr.title,
            "performer": attr.performer,
            "waveform": attr.waveform
        }
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeCustomEmoji):
        return {
            "_": "document.attribute.custom_emoji",
            "alt": attr.alt,
            "stickerset": InputStickerSet(attr.stickerset),
            "free": attr.free,
            "text_color": attr.text_color
        }
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeFilename):
        return {
            "_": "document.attribute.filename",
            "file_name": attr.file_name
        }
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeHasStickers):
        return {
            "_": "document.attribute.has_stickers"
        }
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeImageSize):
        return {
            "_": "document.attribute.image_size"
        }
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeSticker):
        return {
            "_": "document.attribute.sticker",
            "stickerset": InputStickerSet(attr.stickerset),
            "mask": attr.mask,
            "mask_coords": MaskCoords(attr.mask_coords)
        }
    if isinstance(attr, pyrogram.raw.types.DocumentAttributeVideo):
        return {
            "_": "document.attribute.video",
            "duration": attr.duration,
            "w": attr.w,
            "h": attr.h,
            "round_message": attr.round_message,
            "supports_streaming": attr.supports_streaming
        }


def PhotoSize(size:pyrogram.raw.base.PhotoSize) -> dict:
    if isinstance(size, pyrogram.raw.types.PhotoCachedSize):
        return {
            "_": "photo_size.cached",
            "type": size.type,
            "w": size.w,
            "h": size.h,
            "bytes": size.bytes
        }
    if isinstance(size, pyrogram.raw.types.PhotoPathSize):
        return {
            "_": "photo_size.path",
            "type": size.type,
            "bytes": size.bytes
        }
    if isinstance(size, pyrogram.raw.types.PhotoSize):
        return {
            "_": "photo_size.photo_size",
            "type": size.type,
            "w": size.w,
            "h": size.h,
            "size": size.size
        }
    if isinstance(size, pyrogram.raw.types.PhotoSizeEmpty):
        return {
            "_": "photo_size.empty",
            "type": size.type
        }
    if isinstance(size, pyrogram.raw.types.PhotoSizeProgressive):
        return {
            "_": "photo_size.progressive",
            "type": size.type,
            "w": size.w,
            "h": size.h,
            "sizes": size.sizes
        }
    if isinstance(size, pyrogram.raw.types.PhotoStrippedSize):
        return {
            "_": "photo_size.stripped",
            "type": size.type,
            "byes": size.bytes
        }

def VideoSize(size:pyrogram.raw.base.VideoSize) -> dict:
    if isinstance(size, pyrogram.raw.types.VideoSize):
        return {
            "_": "video_size.video_size",
            "type": size.type,
            "w": size.w,
            "h": size.h,
            "size": size.size,
            "video_start_ts": size.video_start_ts
        }
    if isinstance(size, pyrogram.raw.types.VideoSizeEmojiMarkup):
        return {
            "_": "video_size.emoji_markup",
            "emoji_id": size.emoji_id,
            "background_colors": size.background_colors
        }
    if isinstance(size, pyrogram.raw.types.VideoSizeStickerMarkup):
        return {
            "_": "video_size.sticker_markup",
            "stickerset": InputStickerSet(size.stickerset),
            "sticker_id": size.sticker_id,
            "background_colors": size.background_colors
        }

def Document(document:pyrogram.raw.base.Document) -> dict:
    if isinstance(document, pyrogram.raw.types.Document):
        return {
            "_": "media.document.document",
            "id": document.id,
            "access_hash": document.access_hash,
            "file_reference": document.file_reference,
            "date": document.date,
            "mime_type": document.mime_type,
            "size": document.size,
            "dc_id": document.dc_id,
            "attributes": [DocumentAttribute(attr) for attr in document.attributes],
            "thumbs": [PhotoSize(size) for size in document.thumbs],
            "video_thumbs": [VideoSize(size) for size in document.video_thumbs]
        }
    if isinstance(document, pyrogram.raw.types.DocumentEmpty):
        return {
            "_": "media.document.empty_document",
            "id": document.id
        }

def Photo(photo:pyrogram.raw.base.Photo) -> dict:
    if isinstance(photo, pyrogram.raw.types.Photo):
        return {
            "_": "photo.photo",
            "id": photo.id,
            "access_hash": photo.access_hash,
            "file_reference": photo.file_reference,
            "date": photo.date,
            "sizes": [PhotoSize(size) for size in photo.sizes],
            "dc_id": photo.dc_id,
            "has_stickers": photo.has_stickers,
            "video_sizes": [VideoSize(size) for size in photo.video_sizes]
        }
    if isinstance(photo, pyrogram.raw.types.PhotoEmpty):
        return {
            "_": "photo.empty",
            "id": photo.id
        }

def GeoPoint(geo:pyrogram.raw.base.GeoPoint) -> dict:
    if isinstance(geo, pyrogram.raw.types.GeoPoint):
        return {
            "_": "geo_point.geo_point",
            "long": geo.long,
            "lat": geo.lat,
            "access_hash": geo.access_hash,
            "accuracy_radius": geo.accuracy_radius
        }
    if isinstance(geo, pyrogram.raw.types.GeoPointEmpty):
        return {
            "_": "geo_point.empty"
        }

def WebDocument(web:pyrogram.raw.base.WebDocument) -> dict:
    if isinstance(web, pyrogram.raw.types.WebDocument):
        return {
            "_": "web_document.web_document",
            "url": web.url,
            "access_hash": web.access_hash,
            "size": web.size,
            "mime_type": web.mime_type,
            "attributes": [DocumentAttribute(attr) for attr in web.attributes]
        }
    if isinstance(web, pyrogram.raw.types.WebDocumentNoProxy):
        return {
            "_": "web_document.web_document_no_proxy",
            "url": web.url,
            "size": web.size,
            "mime_type": web.mime_type,
            "attributes": [DocumentAttribute(attr) for attr in web.attributes]
        }

def MessageExtendedMedia(media:pyrogram.raw.base.MessageExtendedMedia) -> dict:
    if isinstance(media, pyrogram.raw.types.MessageExtendedMedia):
        return {
            "_": "extended_media.extended_media",
            "media": MessageMedia(media.media)
        }
    if isinstance(media, pyrogram.raw.types.MessageExtendedMediaPreview):
        return {
            "_": "extended_media.preview",
            "w": media.w,
            "h": media.h,
            "thumb": PhotoSize(media.thumb),
            "video_duration": media.video_duration
        }

def PollAnswer(answer:pyrogram.raw.base.PollAnswer) -> dict:
    if isinstance(answer, pyrogram.raw.types.PollAnswer):
        return {
            "_": "poll_answer",
            "text": answer.text,
            "option": answer.option
        }

def Poll(poll:pyrogram.raw.base.Poll) -> dict:
    if isinstance(poll, pyrogram.raw.types.Poll):
        return {
            "_": "poll.poll",
            "id": poll.id,
            "question": poll.question,
            "answers": [PollAnswer(answer) for answer in poll.answers],
            "closed": poll.closed,
            "public_voters": poll.public_voters,
            "multiple_choice": poll.multiple_choice,
            "quiz": poll.quiz,
            "close_period": poll.close_period,
            "close_date": poll.close_date
        }

def PollAnswerVoters(voters:pyrogram.raw.base.PollAnswerVoters) -> dict:
    if isinstance(voters, pyrogram.raw.types.PollAnswerVoters):
        return {
            "_": "poll_answer_voters.poll_answer_voters",
            "option": voters.option,
            "voters": voters.voters,
            "chosen": voters.chosen,
            "correct": voters.correct
        }

def PollResults(results:pyrogram.raw.base.PollResults) -> dict:
    if isinstance(results, pyrogram.raw.types.PollResults):
        return {
            "_": "poll_results.poll_results",
            "min": results.min,
            "results": [PollAnswerVoters(voters) for voters in results.results],
            "total_voters": results.total_voters,
            "recent_voters": results.recent_voters,
            "solution": results.solution
        }

def PageBlock(block:pyrogram.raw.base.PageBlock) -> dict:
    return json.loads(str(block)) if block else None

def Page(page:pyrogram.raw.base.Page) -> dict:
    if isinstance(page, pyrogram.raw.types.Page):
        return {
            "_": "page.page",
            "url": page.url,
            "blocks": [PageBlock(block) for block in page.blocks],
            "photos": [Photo(photo) for photo in page.photos],
            "documents": [Document(document) for document in page.documents],
            "part": page.part,
            "rtl": page.rtl,
            "v2": page.v2,
            "views": page.views
        }

def WallPaperSettings(settings:pyrogram.raw.base.WallPaperSettings) -> dict:
    if isinstance(settings, pyrogram.raw.types.WallPaperSettings):
        return {
            "_": "wallpaper_settings.wallpaper_settings",
            "blur": settings.blur,
            "motion": settings.motion,
            "background_color": settings.background_color,
            "second_background_color": settings.second_background_color,
            "third_background_color": settings.third_background_color,
            "fourth_backround_color": settings.fourth_background_color,
            "intensity": settings.intensity,
            "rotation": settings.rotation
        }

def WallPaper(wallpaper:pyrogram.raw.base.WallPaper) -> dict:
    if isinstance(wallpaper, pyrogram.raw.types.WallPaper):
        return {
            "_": "wallpaper.wallpaper",
            "id": wallpaper.id,
            "access_hash": wallpaper.access_hash,
            "slug": wallpaper.slug,
            "document": Document(wallpaper.document),
            "creator": wallpaper.creator,
            "default": wallpaper.default,
            "pattern": wallpaper.pattern,
            "dark": wallpaper.dark,
            "settings": WallPaperSettings(wallpaper.settings)
        }
    if isinstance(wallpaper, pyrogram.raw.types.WallPaperNoFile):
        return {
            "_": "wallpaper.no_file",
            "id": wallpaper.id,
            "default": wallpaper.default,
            "dark": wallpaper.dark,
            "settings": WallPaperSettings(wallpaper.settings)
        }

def BaseTheme(theme:pyrogram.raw.base.BaseTheme) -> dict:
    if isinstance(theme, pyrogram.raw.types.BaseThemeArctic):
        return {
            "_": "base_theme.arctic"
        }
    if isinstance(theme, pyrogram.raw.types.BaseThemeClassic):
        return {
            "_": "base_theme.classic"
        }
    if isinstance(theme, pyrogram.raw.types.BaseThemeDay):
        return {
            "_": "base_theme.day"
        }
    if isinstance(theme, pyrogram.raw.types.BaseThemeNight):
        return {
            "_": "base_theme.night"
        }
    if isinstance(theme, pyrogram.raw.types.BaseThemeTinted):
        return {
            "_": "base_theme.tinted"
        }

def ThemeSettings(settings:pyrogram.raw.base.ThemeSettings) -> dict:
    if isinstance(settings, pyrogram.raw.types.ThemeSettings):
        return {
            "_": "theme_settings.theme_settings",
            "base_theme": BaseTheme(settings.base_theme),
            "message_colors_animated": settings.message_colors_animated,
            "outbox_accent_color": settings.outbox_accent_color,
            "message_colors": settings.message_colors,
            "wallpaper": WallPaper(settings.wallpaper)
        }

def WebPageAttribute(attr:pyrogram.raw.base.WebPageAttribute) -> dict:
    if isinstance(attr, pyrogram.raw.types.WebPageAttributeTheme):
        return {
            "_": "web_page_attribute.web_page_attribute_theme",
            "documents": [Document(document) for document in attr.documents],
            "settings": ThemeSettings(attr.settings)
        }

def WebPage(webpage:pyrogram.raw.base.WebPage) -> dict:
    if isinstance(webpage, pyrogram.raw.types.WebPage):
        return {
            "_": "webpage.webpage",
            "id": webpage.id,
            "url": webpage.url,
            "display_url": webpage.display_url,
            "hash": webpage.hash,
            "type": webpage.type,
            "site_name": webpage.site_name,
            "title": webpage.title,
            "description": webpage.description,
            "photo": Photo(webpage.photo),
            "embed_url": webpage.embed_url,
            "embed_type": webpage.embed_type,
            "embed_width": webpage.embed_width,
            "embed_height": webpage.embed_height,
            "duration": webpage.duration,
            "author": webpage.author,
            "document": Document(webpage.document),
            "cached_page": Page(webpage.cached_page),
            "attributes": [WebPageAttribute(attr) for attr in webpage.attributes]
        }

def MessageMedia(media:pyrogram.raw.base.MessageMedia) -> dict:
    if isinstance(media, pyrogram.raw.types.MessageMediaContact):
        return {
            "_": "media.contact",
            "phone_number": media.phone_number,
            "first_name": media.first_name,
            "last_name": media.last_name,
            "vcard": media.vcard,
            "user_id": media.user_id
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaDice):
        return {
            "_": "media.dice",
            "value": media.value,
            "emoticon": media.emoticon
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaDocument):
        return {
            "_": "media.document",
            "nopremium": media.nopremium,
            "spoiler": media.spoiler,
            "document": Document(media.document),
            "ttl_seconds": media.ttl_seconds
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaEmpty):
        return {
            "_": "media.empty"
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaGame):
        return {
            "_": "media.game",
            "game": {
                "_": "game",
                "id": media.game.id,
                "access_hash": media.game.access_hash,
                "short_name": media.game.short_name,
                "title": media.game.title,
                "description": media.game.description,
                "photo": Photo(media.game.photo),
                "document": Document(media.game.document)
            }
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaGeo):
        return {
            "_": "media.geo",
            "geo": GeoPoint(media.geo)
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaGeoLive):
        return {
            "_": "media.geo_live",
            "geo": GeoPoint(media.geo),
            "period": media.period,
            "heading": media.heading,
            "proximity_notification_radius": media.proximity_notification_radius
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaInvoice):
        return {
            "_": "media.invoice",
            "title": media.title,
            "description": media.description,
            "currency": media.currency,
            "total_amount": media.total_amount,
            "start_param": media.start_param,
            "shipping_address_requested": media.shipping_address_requested,
            "test": media.test,
            "photo": WebDocument(media.photo),
            "receipt_msg_id": media.receipt_msg_id,
            "extended_media": MessageExtendedMedia(media.extended_media)
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaPhoto):
        return {
            "_": "media.photo",
            "spoiler": media.spoiler,
            "photo": Photo(media.photo),
            "ttl_seconds": media.ttl_seconds
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaPoll):
        return {
            "_": "media.poll",
            "poll": Poll(media.poll),
            "results": PollResults(media.results)
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaUnsupported):
        return {
            "_": "media.unsupported"
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaVenue):
        return {
            "_": "media.venue",
            "geo": GeoPoint(media.geo),
            "title": media.title,
            "address": media.address,
            "provider": media.provider,
            "venue_id": media.venue_id,
            "venue_type": media.venue_type
        }
    if isinstance(media, pyrogram.raw.types.MessageMediaWebPage):
        return {
            "_": "media.web_page",
            "webpage": WebPage(media.webpage)
        }

def InputPeer(peer:pyrogram.raw.base.InputPeer) -> dict:
    if isinstance(peer, pyrogram.raw.types.InputPeerChannel):
        return {
            "_": "input_peer.channel",
            "channel_id": peer.channel_id,
            "access_hash": peer.access_hash
        }
    if isinstance(peer, pyrogram.raw.types.InputPeerChannelFromMessage):
        return {
            "_": "input_peer.channel_from_message",
            "peer": InputPeer(peer.peer),
            "msg_id": peer.msg_id,
            "channel_id": peer.channel_id
        }
    if isinstance(peer, pyrogram.raw.types.InputPeerChat):
        return {
            "_": "input_peer.chat",
            "chat_id": peer.chat_id
        }
    if isinstance(peer, pyrogram.raw.types.InputPeerEmpty):
        return {
            "_": "input_peer.empty"
        }
    if isinstance(peer, pyrogram.raw.types.InputPeerSelf):
        return {
            "_": "input_peer.self"
        }
    if isinstance(peer, pyrogram.raw.types.InputPeerUser):
        return {
            "_": "input_peer.user",
            "user_id": peer.user_id,
            "access_hash": peer.access_hash
        }
    if isinstance(peer, pyrogram.raw.types.InputPeerUserFromMessage):
        return {
            "_": "input_peer.user_from_message",
            "peer": InputPeer(peer.peer),
            "msg_id": peer.msg_id,
            "user_id": peer.user_id
        }

def InputUser(user:pyrogram.raw.base.InputUser) -> dict:
    if isinstance(user, pyrogram.raw.types.InputUser):
        return {
            "_": "input_user.input_user",
            "user_id": user.user_id,
            "access_hash": user.access_hash
        }
    if isinstance(user, pyrogram.raw.types.InputUserEmpty):
        return {
            "_": "input_user.empty"
        }
    if isinstance(user, pyrogram.raw.types.InputUserFromMessage):
        return {
            "_": "input_user.from_message",
            "peer": InputPeer(user.peer),
            "msg_id": user.msg_id,
            "user_id": user.user_id
        }
    if isinstance(user, pyrogram.raw.types.InputUserSelf):
        return {
            "_": "input_user.self"
        }

def MessageEntity(entity:pyrogram.raw.base.MessageEntity) -> dict:
    if isinstance(entity, pyrogram.raw.types.InputMessageEntityMentionName):
        return {
            "_": "message_entity.mention_name",
            "offset": entity.offset,
            "length": entity.length,
            "user_id": InputUser(entity.user_id)
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityBankCard):
        return {
            "_": "message_entity.blank_card",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityBlockquote):
        return {
            "_": "message_entity.blockquote",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityBold):
        return {
            "_": "message_entity.bold",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityBotCommand):
        return {
            "_": "message_entity.command",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityCashtag):
        return {
            "_": "message_entity.cashtag",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityCode):
        return {
            "_": "message_entity.code",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityCustomEmoji):
        return {
            "_": "message_entity.custom_emoji",
            "offset": entity.offset,
            "length": entity.length,
            "document_id": entity.document_id
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityEmail):
        return {
            "_": "message_entity.email",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityHashtag):
        return {
            "_": "message_entity.hashtag",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityItalic):
        return {
            "_": "message_entity.italic",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityMention):
        return {
            "_": "message_entity.mention",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityMentionName):
        return {
            "_": "message_entity.mention_name",
            "offset": entity.offset,
            "length": entity.length,
            "user_id": entity.user_id
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityPhone):
        return {
            "_": "message_entity.phone",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityPre):
        return {
            "_": "message_entity.pre",
            "offset": entity.offset,
            "length": entity.length,
            "language": entity.language
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntitySpoiler):
        return {
            "_": "message_entity.spoiler",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityStrike):
        return {
            "_": "message_entity.strike",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityTextUrl):
        return {
            "_": "message_entity.text_url",
            "offset": entity.offset,
            "length": entity.length,
            "url": entity.url
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityUnderline):
        return {
            "_": "message_entity.underline",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityUnknown):
        return {
            "_": "message_entity.unkown",
            "offset": entity.offset,
            "length": entity.length
        }
    if isinstance(entity, pyrogram.raw.types.MessageEntityUrl):
        return {
            "_": "message_entity.url",
            "offset": entity.offset,
            "length": entity.length
        }

def MessageFwdHeader(header:pyrogram.raw.base.MessageFwdHeader) -> dict:
    if isinstance(header, pyrogram.raw.types.MessageFwdHeader):
        return {
            "_": "message_fwd_header",
            "date": header.date,
            "imported": header.imported,
            "from_id": Peer(header.from_id),
            "from_name": header.from_name,
            "channel_post": header.channel_post,
            "post_author": header.post_author,
            "saved_from_peer": Peer(header.saved_from_peer),
            "saved_from_msg_id": header.saved_from_msg_id,
            "psa_type": header.psa_type
        }

def MessageReplyHeader(header:pyrogram.raw.base.MessageReplyHeader) -> dict:
    if isinstance(header, pyrogram.raw.types.MessageReplyHeader):
        return {
            "_": "message_reply_header.message_reply_header",
            "reply_to_msg_id": header.reply_to_msg_id,
            "reply_to_scheduled": header.reply_to_scheduled,
            "forum_topic": header.forum_topic,
            "reply_to_peer_id": Peer(header.reply_to_peer_id),
            "reply_to_top_id": header.reply_to_top_id
        }

def MessageReplies(replies:pyrogram.raw.base.MessageReplies) -> dict:
    if isinstance(replies, pyrogram.raw.types.MessageReplies):
        return {
            "_": "message_replies.message_replies",
            "replies": replies.replies,
            "replies_pts": replies.replies_pts,
            "comments": replies.comments,
            "recent_repliers": [Peer(replier) for replier in replies.recent_repliers],
            "channel_id": replies.channel_id,
            "max_id": replies.max_id,
            "read_max_id": replies.read_max_id
        }

def Reaction(reaction:pyrogram.raw.base.Reaction) -> dict:
    if isinstance(reaction, pyrogram.raw.types.ReactionCustomEmoji):
        return {
            "_": "reaction.custom_emoji",
            "document_id": reaction.document_id
        }
    if isinstance(reaction, pyrogram.raw.types.ReactionEmoji):
        return {
            "_": "reaction.emoji",
            "emoticon": reaction.emoticon
        }
    if isinstance(reaction, pyrogram.raw.types.ReactionEmpty):
        return {
            "_": "reaction.empty"
        }

def ReactionCount(count:pyrogram.raw.base.ReactionCount) -> dict:
    if isinstance(count, pyrogram.raw.types.ReactionCount):
        return {
            "_": "reaction_count.reaction_count",
            "reaction": Reaction(count.reaction),
            "count": count.count,
            "chosen_order": count.chosen_order
        }

def MessagePeerReaction(reaction:pyrogram.raw.base.MessagePeerReaction) -> dict:
    if isinstance(reaction, pyrogram.raw.types.MessagePeerReaction):
        return {
            "_": "message_peer_reaction.message_peer_reaction",
            "peer_id": Peer(reaction.peer_id),
            "date": reaction.date,
            "reaction": Reaction(reaction.reaction),
            "big": reaction.big,
            "unread": reaction.unread
        }

def MessageReactions(reactions:pyrogram.raw.base.MessageReactions) -> dict:
    if isinstance(reactions, pyrogram.raw.types.MessageReactions):
        return {
            "_": "message_reactions.message_reactions",
            "results": [ReactionCount(count) for count in reactions.results],
            "min": reactions.min,
            "can_see_list": reactions.can_see_list,
            "recent_reactions": [MessagePeerReaction(reaction) for reaction in reactions.recent_reactions]
        }

def ReplyMarkup(markup:pyrogram.raw.base.ReplyMarkup) -> dict:
    return json.loads(str(markup)) if markup else None

def Message(msg:pyrogram.raw.base.Message) -> dict:
    if isinstance(msg, pyrogram.raw.types.Message):
        return {
            "_": "message.message",
            "id": msg.id,
            "peer_id": Peer(msg.peer_id),
            "date": msg.date,
            "message": msg.message,
            "out": msg.out,
            "mentioned": msg.mentioned,
            "media_unread": msg.media_unread,
            "silent": msg.silent,
            "post": msg.post,
            "from_scheduled": msg.from_scheduled,
            "legacy": msg.legacy,
            "edit_hide": msg.edit_hide,
            "pinned": msg.pinned,
            "noforwards": msg.noforwards,
            "from_id": Peer(msg.from_id),
            "fwd_from": MessageFwdHeader(msg.fwd_from),
            "via_bot_id": msg.via_bot_id,
            "reply_to": MessageReplyHeader(msg.reply_to),
            "media": MessageMedia(msg.media),
            "reply_markup": ReplyMarkup(msg.reply_markup),
            "entities": [MessageEntity(entity) for entity in msg.entities],
            "views": msg.views,
            "forwards": msg.forwards,
            "replies": MessageReplies(msg.replies),
            "edit_date": msg.edit_date,
            "post_author": msg.post_author,
            "grouped_id": msg.grouped_id,
            "reactions": MessageReactions(msg.reactions),
            "restriction_reason": [RestrictionReason(reason) for reason in msg.restriction_reason],
            "ttl_period": msg.ttl_period
        }
    if isinstance(msg, pyrogram.raw.types.MessageService):
        return {
            "_": "message.service",
            "id": msg.id,
            "peer_id": Peer(msg.peer_id),
            "date": msg.date,
            "action": MessageAction(msg.action),
            "out": msg.out,
            "mentioned": msg.mentioned,
            "media_unread": msg.media_unread,
            "silent": msg.silent,
            "post": msg.post,
            "legacy": msg.legacy,
            "from_id": Peer(msg.peer_id),
            "reply_to": MessageReplyHeader(msg.reply_to),
            "ttl_period": msg.ttl_period
        }
    if isinstance(msg, pyrogram.raw.types.MessageEmpty):
        return {
            "_": "message.empty",
            "id": msg.id,
            "peer_id": Peer(msg.peer_id)
        }

def BotApp(bot:pyrogram.raw.base.BotApp) -> dict:
    if isinstance(bot, pyrogram.raw.types.BotApp):
        return {
            "_": "bot_app.bot_app",
            "id": bot.id,
            "access_hash": bot.access_hash,
            "short_name": bot.short_name,
            "title": bot.title,
            "description": bot.description,
            "photo": Photo(bot.photo),
            "hash": bot.hash,
            "document": Document(bot.document)
        }
    if isinstance(bot, pyrogram.raw.types.BotAppNotModified):
        return {
            "_": "bot_app.not_modified"
        }

def InputGroupCall(call:pyrogram.raw.base.InputGroupCall) -> dict:
    if isinstance(call, pyrogram.raw.types.InputGroupCall):
        return {
            "_": "input_group_call.input_group_call",
            "id": call.id,
            "access_hash": call.access_hash
        }

def MessageAction(action:pyrogram.raw.base.MessageAction) -> dict:
    if isinstance(action, pyrogram.raw.types.MessageActionBotAllowed):
        return {
            "_": "message_action.bot_allowed",
            "attach_menu": action.attach_menu,
            "domain": action.domain,
            "app": BotApp(action.app)
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChannelCreate):
        return {
            "_": "message_action.channel_create",
            "title": action.title
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChannelMigrateFrom):
        return {
            "_": "message_action.channel_migrate_from",
            "title": action.title,
            "chat_id": action.chat_id
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatAddUser):
        return {
            "_": "message_action.chat_add_user",
            "users": action.users
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatCreate):
        return {
            "_": "message_action.chat_create",
            "title": action.title,
            "users": action.users
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatDeletePhoto):
        return {
            "_": "message_action.chat_delete_photo",
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatDeleteUser):
        return {
            "_": "message_action.chat_delete_user",
            "user_id": action.user_id
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatEditPhoto):
        return {
            "_": "message_action.chat_edit_photo",
            "photo": Photo(action.photo)
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatEditTitle):
        return {
            "_": "message_action.chat_edit_title",
            "title": action.title
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatJoinedByLink):
        return {
            "_": "message_action.chat_joined_by_link",
            "inviter_id": action.inviter_id
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatJoinedByRequest):
        return {
            "_": "message_action.chat_joined_by_request"
        }
    if isinstance(action, pyrogram.raw.types.MessageActionChatMigrateTo):
        return {
            "_": "message_action.chat_migrate_to",
            "channel_id": action.channel_id
        }
    if isinstance(action, pyrogram.raw.types.MessageActionContactSignUp):
        return {
            "_": "message_action.contact_sign_up"
        }
    if isinstance(action, pyrogram.raw.types.MessageActionCustomAction):
        return {
            "_": "message_action.custom_action",
            "message": action.message
        }
    if isinstance(action, pyrogram.raw.types.MessageActionEmpty):
        return {
            "_": "message_action.empty"
        }
    if isinstance(action, pyrogram.raw.types.MessageActionGameScore):
        return {
            "_": "message_action.game_score",
            "game_id": action.game_id,
            "score": action.score
        }
    if isinstance(action, pyrogram.raw.types.MessageActionGeoProximityReached):
        return {
            "_": "message_action.geo_proximity_reached",
            "from_id": Peer(action.from_id),
            "to_id": Peer(action.to_id),
            "distance": action.distance
        }
    if isinstance(action, pyrogram.raw.types.MessageActionGiftPremium):
        return {
            "_": "message_action.gift_premium",
            "currency": action.currency,
            "amount": action.amount,
            "months": action.months,
            "crypto_currency": action.crypto_currency,
            "crypto_amount": action.crypto_amount
        }
    if isinstance(action, pyrogram.raw.types.MessageActionGroupCall):
        return {
            "_": "message_action.group_call",
            "call": InputGroupCall(action.call),
            "duration": action.duration
        }
    if isinstance(action, pyrogram.raw.types.MessageActionGroupCallScheduled):
        return {
            "_": "message_action.group_call_scheduled",
            "call": InputGroupCall(action.call),
            "schedule_date": action.schedule_date
        }
    if isinstance(action, pyrogram.raw.types.MessageActionHistoryClear):
        return {
            "_": "message_action.history_clear"
        }
    if isinstance(action, pyrogram.raw.types.MessageActionInviteToGroupCall):
        return {
            "_": "message_action.invite_to_group_call",
            "call": InputGroupCall(action.call),
            "users": action.users
        }
    if isinstance(action, pyrogram.raw.types.MessageActionPaymentSent):
        return {
            "_": "message_action.payment_sent",
            "currency": action.currency,
            "total_amount": action.total_amount,
            "recurring_init": action.recurring_init,
            "recurring_used": action.recurring_used,
            "invoice_slug": action.invoice_slug
        }
    if isinstance(action, pyrogram.raw.types.MessageActionPaymentSentMe):
        return {
            "_": "message_action.payment_sent_me",
            "currency": action.currency,
            "total_amount": action.total_amount,
            "payload": action.payload,
            "charge": PaymentCharge(action.charge),
            "recurring_init": action.recurring_init,
            "recurring_used": action.recurring_used,
            "info": PaymentRequestedInfo(action.info),
            "shipping_option_id": action.shipping_action_id
        }
    if isinstance(action, pyrogram.raw.types.MessageActionPhoneCall):
        return {
            "_": "message_action.phone_call",
            "call_id": action.call_id,
            "video": action.video,
            "reason": PhoneCallDiscardReason(action.reason),
            "duration": action.duration
        }
    if isinstance(action, pyrogram.raw.types.MessageActionPinMessage):
        return {
            "_": "message_action.pin_message"
        }
    if isinstance(action, pyrogram.raw.types.MessageActionRequestedPeer):
        return {
            "_": "message_action.requested_peer",
            "button_id": action.button_id,
            "peer": Peer(action.peer)
        }
    if isinstance(action, pyrogram.raw.types.MessageActionScreenshotTaken):
        return {
            "_": "message_action.screenshot_taken"
        }
    return json.loads(str(action)) if action else None

def PhoneCallDiscardReason(reason:pyrogram.raw.base.PhoneCallDiscardReason) -> dict:
    if isinstance(reason, pyrogram.raw.types.PhoneCallDiscardReasonBusy):
        return {
            "_": "phone_call_discard_reason.busy"
        }
    if isinstance(reason, pyrogram.raw.types.PhoneCallDiscardReasonDisconnect):
        return {
            "_": "phone_call_discard_reason.disconnect"
        }
    if isinstance(reason, pyrogram.raw.types.PhoneCallDiscardReasonHangup):
        return {
            "_": "phone_call_discard_reason.hangup"
        }
    if isinstance(reason, pyrogram.raw.types.PhoneCallDiscardReasonMissed):
        return {
            "_": "phone_call_discard_reason.missed"
        }

def PaymentCharge(charge:pyrogram.raw.base.PaymentCharge) -> dict:
    if isinstance(charge, pyrogram.raw.types.PaymentCharge):
        return {
            "_": "payment_charge.payment_charge",
            "id": charge.id,
            "provider_charge_id": charge.provider_charge_id
        }

def PaymentRequestedInfo(info:pyrogram.raw.base.PaymentRequestedInfo) -> dict:
    if isinstance(info, pyrogram.raw.types.PaymentRequestedInfo):
        return {
            "_": "payment_requested_info.payment_requested_info",
            "name": info.name,
            "phone": info.phone,
            "email": info.email,
            "shipping_address": PostAddress(info.shipping_address)
        }

def PostAddress(addr:pyrogram.raw.base.PostAddress) -> dict:
    if isinstance(addr, pyrogram.raw.types.PostAddress):
        return {
            "_": "post_address.post_address",
            "street_line1": addr.street_line1,
            "street_line2": addr.street_line2,
            "city": addr.city,
            "state": addr.state,
            "country_iso2": addr.country_iso2,
            "post_code": addr.post_code
        }

def ChatPhoto(photo:pyrogram.raw.base.ChatPhoto) -> dict:
    if isinstance(photo, pyrogram.raw.types.ChatPhoto):
        return {
            "_": "chat_photo.chat_photo",
            "photo_id": photo.photo_id,
            "dc_id": photo.dc_id,
            "has_video": photo.has_video,
            "stripped_thumb": photo.stripped_thumb
        }
    if isinstance(photo, pyrogram.raw.types.ChatPhotoEmpty):
        return {
            "_": "chat_photo.empty"
        }

def Folder(folder:pyrogram.raw.base.Folder) -> dict:
    if isinstance(folder, pyrogram.raw.types.Folder):
        return {
            "_": "folder.folder",
            "id": folder.id,
            "title": folder.title,
            "autofill_new_broadcasts": folder.autofill_new_broadcasts,
            "autofill_public_groups": folder.autofill_public_groups,
            "autofill_new_correspondents": folder.autofill_new_correspondents,
            "photo": ChatPhoto(folder.photo)
        }

def Dialog(dialog:pyrogram.raw.base.Dialog, top_message:pyrogram.raw.base.Message) -> dict:
    if isinstance(dialog, pyrogram.raw.types.Dialog):
        return {
            "_": "dialog.dialog",
            "peer": Peer(dialog.peer),
            "top_message": Message(top_message),
            "read_inbox_max_id": dialog.read_inbox_max_id,
            "read_outbox_max_id": dialog.read_outbox_max_id,
            "unread_count": dialog.unread_count,
            "unread_mentions_count": dialog.unread_mentions_count,
            "unread_reactions_count": dialog.unread_reactions_count,
            "pinned": dialog.pinned,
            "unread_mark": dialog.unread_mark
        }
    if isinstance(dialog, pyrogram.raw.types.DialogFolder):
        return {
            "_": "dialog.folder",
            "peer": Peer(dialog.peer),
            "top_message": Message(top_message),
            "unread_muted_peers_count": dialog.unread_muted_peers_count,
            "unread_unmuted_peers_count": dialog.unread_unmuted_peers_count,
            "unread_muted_messages_count": dialog.unread_muted_messages_count,
            "unread_unmuted_messages_count": dialog.unread_unmuted_messages_count,
            "pinned": dialog.pinned
        }

def DialogPeer(peer:pyrogram.raw.base.DialogPeer) -> dict:
    if isinstance(peer, pyrogram.raw.types.DialogPeer):
        return {
            "_": "dialog_peer.dialog_peer",
            "peer": Peer(peer.peer)
        }
    if isinstance(peer, pyrogram.raw.types.DialogPeerFolder):
        return {
            "_": "dialog_peer.folder",
            "folder_id": peer.folder_id
        }