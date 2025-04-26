from aiogram.types import Message
from loguru import logger

import env
from config import bot


@logger.catch
async def edit_message_in_channel(text: str) -> Message | bool:
    return await bot.edit_message_text(
        text=text,
        chat_id=env.TELEGRAM_BOT_CHANNEL_ID,
        message_id=env.TELEGRAM_BOT_MESSAGE_ID,
    )


@logger.catch
async def send_message_in_channel(text: str) -> Message:
    return await bot.send_message(
        chat_id=env.TELEGRAM_BOT_CHANNEL_ID, text=text
    )
