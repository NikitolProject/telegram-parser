from django.urls import path
from django.views.generic import RedirectView

from app.views import start_parse, start_malling


urlpatterns = [
    path('parse/', start_parse, name='start parse'),
    path('malling/', start_malling, name='start mailing')
]
