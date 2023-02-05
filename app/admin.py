from django.contrib import admin
from django.shortcuts import render, redirect

from app.forms import ParserForm
from app.models import TelegramChannel, TelegramUser
from app.decorators import action_form

# my_action.short_description = "Update selected articles"


class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_id_tag', 'title_tag')
    actions = ['my_action']

    @action_form(ParserForm)
    def my_action(modeladmin, request, queryset, form):
        post_count = form.cleaned_data['post_count']

        print(post_count)


# Register your models here.
admin.site.register(TelegramChannel, TelegramChannelAdmin)    
admin.site.register(TelegramUser)
