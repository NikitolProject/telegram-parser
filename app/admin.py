from django.contrib import admin
from django.shortcuts import render, redirect

from app.forms import ParserForm, MailingForm
from app.models import TelegramChannel, TelegramUser
from app.decorators import action_parser_form, action_malling_form

# my_action.short_description = "Update selected articles"


class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_id_tag', 'title_tag')
    actions = ['start_parser']

    @action_parser_form(ParserForm)
    def start_parser(modeladmin, request, queryset, form):
        pass


class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_id_tag', 'title_tag')
    actions = ['start_malling']

    @action_malling_form(MailingForm)
    def start_malling(modeladmin, request, queryset, form):
        pass


# Register your models here.
admin.site.register(TelegramChannel, TelegramChannelAdmin)    
admin.site.register(TelegramUser)
