from django.core.management.base import BaseCommand

from telethon.tl.types import PeerChannel, PeerUser

from app.models import TelegramUser


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
        print(PeerUser(int(TelegramUser.objects.last().user_id.replace('PeerUser(user_id=', '').replace(')', ''))))
