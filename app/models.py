from django.db import models


class TelegramUser(models.Model):

    class Meta:
        db_table = "TelegramUser"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    user_id = models.IntegerField()
    username = models.CharField(max_length=255, null=True, blank=True)

    def user_id_tag(self: "TelegramUser") -> int:
        return self.user_id
    
    user_id_tag.short_description = "ID пользователя"

    def username_tag(self: "TelegramUser") -> str:
        return self.username
    
    username_tag.short_description = "Username пользователя"


class TelegramChannel(models.Model):

    class Meta:
        db_table = "TelegramChannel"
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    channel_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255)

    def channel_id_tag(self: "TelegramUser") -> int:
        return self.channel_id
    
    channel_id_tag.short_description = "ID канала"

    def title_tag(self: "TelegramUser") -> str:
        return self.title
    
    title_tag.short_description = "Название канала"

    def url_tag(self: "TelegramUser") -> str:
        return self.url
    
    url_tag.short_description = "Ссылка на канал"
