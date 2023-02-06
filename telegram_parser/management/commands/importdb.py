import csv

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
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
        with open("members.csv") as fp:
            reader = csv.reader(fp, delimiter="\n")
            # next(reader, None)  # skip the headers
            data_read = [(row.split(".")[0], row.split(".")[1]) for row in reader]

        users = []

        for row in data_read:
            users.append(TelegramUser(user_id=row[0], user_name=row[1]))

        TelegramUser.objects.bulk_create(users)
