import random
from datetime import datetime

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiohttp import ClientSession
from loguru import logger

import env
from config import bot, redis_client


@logger.catch
async def redis_get_key(key: str) -> str | None:
    value = await redis_client.get(key)
    if not value:
        return None
    return value


@logger.catch
async def redis_set_key(key: str, value: str | int) -> None:
    await redis_client.set(key, value)


def get_current_date() -> str:
    datetime_now = datetime.now(tz=env.TIMEZONE)
    return datetime_now.date().strftime('%d.%m.%Y')


def get_current_datetime() -> str:
    datetime_now = datetime.now(tz=env.TIMEZONE)
    return datetime_now.strftime('%d.%m.%Y в %H:%M:%S')


@logger.catch
async def edit_message_in_channel(text: str) -> Message | bool:
    message_id = await redis_get_key('message_id')
    try:
        return await bot.edit_message_text(
            text=text,
            chat_id=env.TELEGRAM_BOT_CHANNEL_ID,
            message_id=message_id,
        )
    except TelegramBadRequest:
        last_message = await redis_get_key('last_message')
        return await send_message_in_channel(
            text=text, last_message=last_message
        )


@logger.catch
async def send_message_in_channel(text: str, last_message: str) -> Message:
    await redis_set_key('last_message', last_message)
    message = await bot.send_message(
        chat_id=env.TELEGRAM_BOT_CHANNEL_ID, text=text
    )
    await redis_set_key('message_id', message.message_id)


@logger.catch
async def make_html_request(url: str) -> str:
    async with ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            return await response.text()


def get_sleep_time() -> int:
    hour_now = datetime.now(env.TIMEZONE).hour
    hour_now = 6
    if 0 <= hour_now < 6:
        return random.randint(3500, 3700)
    else:
        return random.randint(1700, 1900)
