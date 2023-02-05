from django.urls import path
from django.views.generic import RedirectView

from app.views import start_parse


urlpatterns = [
    path('parse/', start_parse, name='start parse'),
]
