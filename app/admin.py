from django.contrib import admin
from django.shortcuts import render, redirect

from asgiref.sync import async_to_sync

from app.forms import ParserForm, MailingForm
from app.models import TelegramChannel, TelegramUser
from app.decorators import action_parser_form, action_malling_form
from app.tasks import get_telegram_channel_info_by_link

# my_action.short_description = "Update selected articles"


class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_id_tag', 'title_tag')
    actions = ['start_parser']

    @action_parser_form(ParserForm)
    def start_parser(modeladmin, request, queryset, form):
        pass

    def save_model(self, request, obj, form, change) -> "TelegramChannel":
        if not change:
            data = async_to_sync(get_telegram_channel_info_by_link)(obj.url)
            print(data)
            obj.channel_id = data[0]
            obj.title = data[1]
            obj.save()
            print("obj saved")

        super().save_model(request, obj, form, change)


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id_tag', 'username_tag')
    actions = ['start_malling']

    @action_malling_form(MailingForm)
    def start_malling(modeladmin, request, queryset, form):
        pass


# Register your models here.
admin.site.register(TelegramChannel, TelegramChannelAdmin)    
admin.site.register(TelegramUser, TelegramUserAdmin)
