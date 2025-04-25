import asyncio
import sys

from loguru import logger

import env
from bot_logging import log_to_telegram_bot
from parsing import parsing_main


async def main():
    logger.remove(0)
    logger.add(sink=sys.stderr)
    logger.add(sink=log_to_telegram_bot, format=env.TELEGRAM_LOGGER_FORMAT)

    logger.info('Telegram bot has started!')

    await parsing_main()


if __name__ == '__main__':
    asyncio.run(main())
