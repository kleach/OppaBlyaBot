import logging

from aiogram.types import (
    Message,
    InputFile,
    ContentTypes,
)

from src.bot.media_db import MediaLinksDB
from src.context import Context
from src.utils.paths import (
    JOINED_MEDIA_SRC_PATH,
    LEFT_MEDIA_SRC_PATH,
)

log = logging.getLogger('Bot')


async def cmd_impl(message: Message, message_type: MediaLinksDB.LinkType, media_src_path: str):
    if Context().media.has_link(message.chat.id, message_type):
        log.info('sending previously uploaded animation')

        await message.reply_animation(Context().media.get_link(message.chat.id, message_type))
        return

    log.info(f'sending animation from local file "{media_src_path}"')

    sent_message: Message = await message.reply_animation(InputFile(media_src_path))
    Context().media.add_link(message.chat.id, message_type, sent_message.animation.file_id)


async def hi(message: Message):
    await cmd_impl(message, MediaLinksDB.LinkType.Joined, JOINED_MEDIA_SRC_PATH)


async def bye(message: Message):
    await cmd_impl(message, MediaLinksDB.LinkType.Left, LEFT_MEDIA_SRC_PATH)


def post_load_cmds():
    log.info('registering handler for "hi"')
    Context().dispatcher.register_message_handler(hi, content_types=ContentTypes.NEW_CHAT_MEMBERS)
    Context().dispatcher.register_message_handler(hi, commands=['hi'])

    log.info('registering handler for "bye"')
    Context().dispatcher.register_message_handler(bye, content_types=ContentTypes.LEFT_CHAT_MEMBER)
    Context().dispatcher.register_message_handler(bye, commands=['bye'])
