import asyncio
import random
from datetime import datetime
from typing import NoReturn

import dotenv
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from loguru import logger

import env
from telegram import edit_message_in_channel, send_message_in_channel

last_message = ''


def get_current_date() -> str:
    datetime_now = datetime.now(tz=env.TIMEZONE)
    return datetime_now.date().strftime('%d.%m.%Y')


def get_current_datetime() -> str:
    datetime_now = datetime.now(tz=env.TIMEZONE)
    return datetime_now.strftime('%d.%m.%Y в %H:%M:%S')


@logger.catch
async def make_html_request(url: str) -> str:
    async with ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            return await response.text()


@logger.catch
async def parse_outages_html(url: str, type_of_outage: str) -> str:
    html = await make_html_request(url)
    soup = BeautifulSoup(html, 'lxml')

    all_addresses = soup.find_all(class_='pd-col4')
    all_outage_periods = soup.find_all(class_='pd-col3')

    message = ''
    message += f'{type_of_outage} отключения:\n\n'

    if not all_addresses or not all_outage_periods:
        return message

    all_addresses.pop(0)
    all_outage_periods.pop(0)

    for n, address in enumerate(all_addresses):
        if env.SEARCH_ADDRESS in address.text.lower():
            period = all_outage_periods[n].text
            if not any(i.isdigit() for i in period):
                period = 'Неизвестно'
            message += f'{address.text}. Период: {period}\n'

    return message


@logger.catch
async def start_parsing() -> NoReturn:
    global last_message

    while True:
        planned_outages_message = await parse_outages_html(
            url=env.PLANNED_OUTAGES_URL, type_of_outage='Плановые'
        )
        emergency_outages_message = await parse_outages_html(
            url=env.EMERGENCY_OUTAGES_URL.format(date=get_current_date()),
            type_of_outage='Аварийные',
        )

        final_message = (
            f'{planned_outages_message}\n\n{emergency_outages_message}'
        )
        if final_message == last_message:
            message_to_send = (
                f'<b>Обновлено {get_current_datetime()}</b>\n\n'
                + final_message
            )
            await edit_message_in_channel(message_to_send)
        else:
            message_to_send = (
                f'<b>Обновлено {get_current_datetime()}</b>\n\n'
                + final_message
            )
            last_message = final_message
            message = await send_message_in_channel(message_to_send)
            env.TELEGRAM_BOT_MESSAGE_ID = message.message_id
            dotenv.set_key(
                '.env',
                'TELEGRAM_BOT_MESSAGE_ID',
                str(message.message_id),
            )

        await asyncio.sleep(random.randint(3500, 3700))
