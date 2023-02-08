import ast
import random
import asyncio
import contextlib

from io import BytesIO
from typing import List, Optional

from channels.db import database_sync_to_async

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.patched import Message
from telethon.tl.types import PeerChannel, PeerUser

from app.models import TelegramChannel, TelegramUser

api_id = 14429679
api_hash = '5a91e2bfd9b57d681a2095b13af3072f'


async def start_parsing(channel_ids: List[int], post_count: int) -> None:
    print("start parse")
    channel_ids = await get_telegram_channels_by_ids(channel_ids=channel_ids)

    client = TelegramClient('79851659771', api_id, api_hash)
    await client.start()

    await parse_for_channels(client, channel_ids, post_count)


async def start_mailing(user_ids: List[int], text: str, file: Optional[bytes] = None) -> None:
    print("start mailing")
    user_names = await get_telegram_users_by_ids(user_ids=user_ids)

    client = TelegramClient('79851659771', api_id, api_hash)
    await client.start()

    await mailing_users(client, user_names, text, file)


async def mailing_users(client: TelegramClient, user_names: List[str], text: str, file: Optional[bytes] = None) -> None:
    print("start mailing users")
    message_count_sent = 0

    for user_name in user_names:
        with contextlib.suppress(Exception):
            user = await client.get_entity(user_name)

            # if file:
            #     with BytesIO(file) as bytes_io:
            #         await client.send_file(user, bytes_io, caption=text)
            # else:
            #     await client.send_message(user, text)

            rand_texts = ['Привет, как дела?', 'Привет, что делаешь?', 'Привет, напиши, как будешь свободен', 'Ты тут? Отпишись, пожалуйста', 'Хай, ты тут?']

            await client.send_message(user, random.choice(rand_texts))
            message_count_sent += 1 if message_count_sent != 48 else 0
            
            await asyncio.sleep(random.randint(13, 60) if message_count_sent != 48 else 5 * 60)

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
