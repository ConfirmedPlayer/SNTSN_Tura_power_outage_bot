import asyncio
from datetime import datetime

from aiohttp import ClientSession
from bs4 import BeautifulSoup

import env
from config import bot


def get_current_date() -> str:
    datetime_now = datetime.now(tz=env.TIMEZONE)
    return datetime_now.date().strftime('%d.%m.%Y')


def get_current_datetime() -> str:
    datetime_now = datetime.now(tz=env.TIMEZONE)
    return datetime_now.strftime('%d.%m.%Y в %H:%M:%S')


async def make_html_request(url: str) -> str:
    async with ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            return await response.text()


async def parse_planned_outages_html() -> str:
    html = await make_html_request(env.PLANNED_OUTAGES_URL)
    soup = BeautifulSoup(html, 'lxml')

    all_addresses = soup.find_all(class_='pd-col4')
    all_outage_periods = soup.find_all(class_='pd-col3')

    current_datetime = get_current_datetime()
    message = f'Обновлено {current_datetime}\n\n'
    message += 'Плановые отключения:\n\n'

    all_addresses.pop(0)
    all_outage_periods.pop(0)

    for n, address in enumerate(all_addresses):
        if env.SEARCH_ADDRESS in address.text.lower():
            period = all_outage_periods[n].text
            if not any(i.isdigit() for i in period):
                period = 'Неизвестно'
            message += f'{address.text}. Период: {period}\n'

    return message


async def parse_emergency_outages_html() -> str:
    url = env.EMERGENCY_OUTAGES_URL.format(date=get_current_date())
    html = await make_html_request(url)
    soup = BeautifulSoup(html, 'lxml')

    all_addresses = soup.find_all(class_='pd-col4')
    all_outage_periods = soup.find_all(class_='pd-col3')

    current_datetime = get_current_datetime()
    message = f'Обновлено {current_datetime}\n\n'
    message += 'Аварийные отключения:\n\n'

    all_addresses.pop(0)
    all_outage_periods.pop(0)

    for n, address in enumerate(all_addresses):
        if env.SEARCH_ADDRESS in address.text.lower():
            period = all_outage_periods[n].text
            if not any(i.isdigit() for i in period):
                period = 'Неизвестно'
            message += f'{address.text}. Период: {period}\n'

    return message


async def edit_message_in_channel(text: str):
    await bot.edit_message_text(
        text=text,
        chat_id=env.TELEGRAM_BOT_CHANNEL_ID,
        message_id=env.TELEGRAM_BOT_MESSAGE_ID,
    )


async def parsing_main():
    while True:
        planned_outages_message = await parse_planned_outages_html()
        emergency_outages_message = await parse_emergency_outages_html()

        final_message = (
            f'{planned_outages_message}\n\n{emergency_outages_message}'
        )

        await edit_message_in_channel(final_message)

        await asyncio.sleep(3600)
