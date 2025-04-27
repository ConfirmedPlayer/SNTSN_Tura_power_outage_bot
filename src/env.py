from os import getenv
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()


PROJECT_NAME = getenv('PROJECT_NAME')


TIMEZONE = ZoneInfo('Asia/Yekaterinburg')


SEARCH_ADDRESS = getenv('SEARCH_ADDRESS')


TELEGRAM_LOGGER_FORMAT = (
    f'{PROJECT_NAME}\n\n'
    '{level} {time:DD.MM.YYYY HH:mm:ss}\n'
    '{name}:{function}\n\n'
    '{message}'
)


TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')

TELEGRAM_BOT_CHANNEL_ID = getenv('TELEGRAM_BOT_CHANNEL_ID')


TELEGRAM_LOGGING_BOT_TOKEN = getenv('TELEGRAM_LOGGING_BOT_TOKEN')

TELEGRAM_LOGGING_CHAT_ID = getenv('TELEGRAM_LOGGING_CHAT_ID')


PLANNED_OUTAGES_URL = 'https://suenco.ru/otklucheniya/elektrosnabzhenie/planovye-otklyucheniya1/tyumen/tyumen/'

EMERGENCY_OUTAGES_URL = 'https://suenco.ru/otklucheniya/elektrosnabzhenie/ekstrennye-otklyucheniya/tyumen/tyumen/?date={date}'
