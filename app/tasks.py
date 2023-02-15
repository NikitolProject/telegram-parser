import ast
import random
import asyncio
import aiohttp
import contextlib
import socks

from io import BytesIO
from typing import List, Optional

from channels.db import database_sync_to_async

from telethon import TelegramClient, errors
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.patched import Message
from telethon.tl.types import PeerChannel, PeerUser

from app.models import TelegramChannel, TelegramUser

api_id = 14429679
api_hash = '5a91e2bfd9b57d681a2095b13af3072f'


def split_list(lst: list, n: int) -> list:
    """
    Разделяет список `lst` на `n` подсписков.
    Если `lst` нельзя разделить на ровное количество подсписков, остаток остается в последнем подсписке.
    """
    split_size = len(lst) // n
    remainder = len(lst) % n

    result = []
    start = 0
    for i in range(n):
        end = start + split_size
        if i < remainder:
            end += 1

        result.append(lst[start:end])
        start = end

    return result


async def start_parsing(channel_ids: List[int], post_count: int) -> None:
    print("start parse")
    channel_ids = await get_telegram_channels_by_ids(channel_ids=channel_ids)

    client = TelegramClient('79851659771', api_id, api_hash)
    await client.start()

    await parse_for_channels(client, channel_ids, post_count)


async def start_mailing(user_ids: List[int], text: str, file: Optional[bytes] = None) -> None:
    print("start mailing")
    user_names = await get_telegram_users_by_ids(user_ids=user_ids)

    user_names_lists = split_list(user_names, 3)
    coroutines = [
        start_session_mailing(session[0], session[1], text, file) 
        for session in [('telethon', user_names_lists[0]), 
                        ('telethon2', user_names_lists[1]), ('telethon3', user_names_lists[2])]
    ]
    await asyncio.gather(*coroutines)


async def start_session_mailing(session: str, user_names: List[str], text: str, file: Optional[bytes] = None) -> None:
    async with TelegramClient(session, api_id, api_hash, proxy=(socks.SOCKS5, '37.18.73.60', 5566)) as client:
        await mailing_users(client, user_names, text, file)


async def mailing_users(client: TelegramClient, user_names: List[str], text: str, file: Optional[bytes] = None) -> None:
    print("start mailing users")
    message_count_sent = 0

    for user_name in user_names:
        if user_name is None or user_name == "None":
            continue

        # with contextlib.suppress(Exception):
        try:
            user = await client.get_entity(user_name)

            # texts = [
            #     "БЕСПЛАТНАЯ СТАВКА НА ФУТБОЛ ⚽️\n\nЗАБРАТЬ ТУТ 👉 https://t.me/+eK4CkR8uCyc5NDZi",
            #     "Закрытый клуб стоимостью 5000₽ бесплатно для первых 40 человек 💰\n\nВСТУПИТЬ БЕСПЛАТНО — https://t.me/+02msrMgQhaJiMWVi",
            #     "📌 Вы выиграли 10.000 рублей!\nИменно столько стоит доступ в наш платный VIP-канал! Кто успеет - останется в нем навсегда!\n\nПоследние 5 сигналов:\n1.98 ✅\n1.63 ✅\n1.49 ✅\n2.85 ✅\n1.76 ✅\n\nПримем БЕСПЛАТНО только 30 человек, дальше вход 10.000₽\n\nЖми 👇 👇 👇\nhttps://t.me/+f_ir2f1oQ1ZlNjMy",
            #     "Сегодня вход в VIP-канал БЕСПЛАТНЫЙ! Кто успеет - останется навсегда в нем!\n\nСтатистика 101✅ 12 -\n\nПримем еще 70 своих людей👇🏻\n\nhttps://t.me/+T2bqvsTeR4w0MWQy",
            #     "Сегодня доступ в VIP-канал БЕСПЛАТНЫЙ! Кто успеет - останется в нем навсенда!\n\nСтатистика 87 ✅ 10 ❌\n\nОсталось 47 бесплатных мест👇🏻\n\nhttps://t.me/+iJIAI2IxuyozNzgy"
            # ]

            # if file:
            #     with BytesIO(file) as bytes_io:
            #         await client.send_file(user, bytes_io, caption=text)
            # else:
            #     await client.send_message(user, text)

            # rand_texts = ['Привет, как дела?', 'Привет, что делаешь?', 'Привет, напиши, как будешь свободен', 'Ты тут? Отпишись, пожалуйста', 'Хай, ты тут?']

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://chestnut-bustling-allspice.glitch.me/api/v1/question', 
                    json={'text': 'Перефразируй: БЕСПЛАТНАЯ СТАВКА НА ФУТБОЛ ⚽️ ЗАБРАТЬ ТУТ 👉 https://t.me/+eK4CkR8uCyc5NDZi'}
                ) as response:
                    text = (await response.json())['answer'].replace("\n\n", "")

            await client.send_message(user, text)
            message_count_sent += 1 if message_count_sent != 48 else 0
            
            print(f"{user_name} получил сообщение!")
            await asyncio.sleep(random.randint(13, 60) if message_count_sent != 48 else 5 * 60)
        except ValueError as exception:
            print(exception)
        except errors.rpcerrorlist.PeerFloodError as exception:
            print(exception)

    admin = await client.get_entity('nick_test_for_bots')
    await client.send_message(admin, f"⚡️ Рассылка на {len(user_names)} пользователей успешно завершена!")

 
async def parse_for_channels(client: TelegramClient, channel_ids: List[int], post_count: int) -> None:
    users = set()

    for channel_id in channel_ids:
        channel = await client.get_entity(PeerChannel(int(channel_id)))

        offset_id = 0
        limit = 100 if post_count >= 100 else post_count
        final_limit = 0 if post_count >= 100 and post_count % 100 == 0 or post_count < 100 else post_count % 100
        current_post_count = post_count

        all_messages = []

        while current_post_count > 0:
            history = await client(
                GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit if post_count >= 100 and current_post_count >= 100 else final_limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                )
            )

            if not history.messages:
                break

            messages = history.messages
            all_messages.extend(messages)
            offset_id = messages[len(messages) - 1].id
            current_post_count -= limit if post_count >= 100 and current_post_count >= 100 or post_count < 100 else final_limit

        offset_id = 0
        limit = 100

        for message in all_messages:
            with contextlib.suppress(Exception):
                if message.replies is None:
                    continue

                while True:
                    messages = await client.get_messages(
                        channel,
                        offset_id=offset_id,
                        offset_date=None,
                        add_offset=0,
                        limit=limit,
                        max_id=0,
                        min_id=0,
                        reply_to=message.id
                    )

                    if not messages:
                        break

                    messages = messages

                    for comment in messages:
                        user = await client.get_entity(comment.from_id)
                        print(f"{user.id},{user.username}")
                        users.add(f"{user.id},{user.username}")
                    
                    offset_id = messages[len(messages) - 1].id

    print("parser completed")
    await create_telegram_users(users)
    print("new users saved.")


async def get_telegram_channel_info_by_link(link: str) -> tuple:
    client = TelegramClient('79851659771', api_id, api_hash)
    await client.start()
    print("start parser")

    await client(JoinChannelRequest(link))
    channel = await client.get_entity(link)
    print(channel)
    print("join channel")

    return (str(channel.id), channel.title)


@database_sync_to_async
def get_telegram_channels_by_ids(channel_ids: List[int]) -> List[int]:
    return [obj.channel_id for obj in TelegramChannel.objects.in_bulk(channel_ids).values()]


@database_sync_to_async
def get_telegram_users_by_ids(user_ids: List[int]) -> List[str]:
    print(user_ids)
    print(type(user_ids))
    if isinstance(user_ids, str) and not user_ids.startswith("["):
        return [obj.username for obj in TelegramUser.objects.in_bulk([int(user_ids)]).values()]
    return [obj.username for obj in TelegramUser.objects.in_bulk([int(uid) for uid in ast.literal_eval(user_ids)]).values()]


@database_sync_to_async
def create_telegram_users(users: List[str]) -> None:
    existing_user_ids = TelegramUser.objects.values_list('user_id', flat=True)
    new_users = [user.split(",") for user in users if user.split(",")[0] not in existing_user_ids]
    TelegramUser.objects.bulk_create([TelegramUser(user_id=user[0], username=user[1]) for user in new_users])
