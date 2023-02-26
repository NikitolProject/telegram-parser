import csv
import time
import random

from django.core.management.base import BaseCommand

from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, PeerUser
from telethon.tl.functions.channels import InviteToChannelRequest

from app.models import TelegramUser

api_id = 3856575
api_hash = '1d6df36bd42c437da9d0ce81dc0f3057'


class Command(BaseCommand):
    """
    This command is needed to create a new administrator account 
    in automatic mode during the deployment of the project via CI/CD.
    """
    help = 'Create SuperUser account'

    def handle(self: "Command", *args: tuple, **options: dict) -> None:
        """
        A command handler that creates an administrator account already based on the specified data.
        """
        client = TelegramClient('79608711591', api_id, api_hash)
        client.start()
        phones = []

        for user in TelegramUser.objects.filter(user_id__contains="PeerUser(user_id="):
            try:
                user_id = PeerUser(int(user.user_id.replace('PeerUser(user_id=', '').replace(')', '')))
                user = client.get_entity(user_id)

                if user.phone is not None:
                    phones.append(user.phone)
                    print(user.phone)
        
            except ValueError:
                print(f"Not found user {user.user_id}")
                continue

        print(len(phones))

        with open("phones.csv", "wt") as fp:
            writer = csv.writer(fp, delimiter="\n")
            # writer.writerow(["your", "header", "foo"])  # write header
            writer.writerow(phones)

        # chat = client.get_entity(PeerChannel(1817095203))

        # invited_users = []

        # for user in users:
        #     invited_users.append(user)

        #     if len(invited_users) == 50:
        #         print(client(InviteToChannelRequest(chat, invited_users)))
        #         time.sleep(random.randint(5, 20))
        #         invited_users = []

        client.disconnect()
