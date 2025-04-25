from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import env

bot = Bot(
    token=env.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


logger_bot = Bot(token=env.TELEGRAM_LOGGING_BOT_TOKEN)
