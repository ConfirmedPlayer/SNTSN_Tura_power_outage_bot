import asyncio
from typing import NoReturn

from bs4 import BeautifulSoup
from loguru import logger

import env
from tools import (
    edit_message_in_channel,
    get_current_date,
    get_current_datetime,
    get_sleep_time,
    make_html_request,
    redis_get_key,
    send_message_in_channel,
)


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
        if final_message == await redis_get_key('last_message'):
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
            await send_message_in_channel(
                text=message_to_send, last_message=final_message
            )

        await asyncio.sleep(get_sleep_time())
