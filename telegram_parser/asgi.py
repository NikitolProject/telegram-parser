"""
ASGI config for telegram_parser project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_parser.settings')

django_asgi_app  = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # Just HTTP for now. (We can add other protocols later.)
    }
)
