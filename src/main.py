import asyncio
import sys

from loguru import logger

import env
from bot_logging import log_to_telegram_bot
from config import redis_client
from parsing import start_parsing


@logger.catch
async def main():
    try:
        logger.remove(0)
        logger.add(sink=sys.stderr)
        logger.add(sink=log_to_telegram_bot, format=env.TELEGRAM_LOGGER_FORMAT)

        logger.info('Telegram bot has started!')

        await start_parsing()
    finally:
        logger.info('Closing redis...')
        await redis_client.aclose(close_connection_pool=True)


if __name__ == '__main__':
    asyncio.run(main())
