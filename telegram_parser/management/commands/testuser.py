from django.core.management.base import BaseCommand

from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, PeerUser

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
        for user in TelegramUser.objects.all().reverse():
            user_id = PeerUser(int(user.user_id.replace('PeerUser(user_id=', '').replace(')', '')))

            client = TelegramClient('79608711591', api_id, api_hash)
            client.start()

            user = client.get_entity(user_id)

            print(user)

            client.disconnect()
