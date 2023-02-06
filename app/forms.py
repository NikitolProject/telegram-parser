from django import forms


class ParserForm(forms.Form):
    title = 'Запуск парсера для сбора пользователей'
    post_count = forms.IntegerField()


class MailingForm(forms.Form):
    title = 'Запуск рассылки на выбранных пользователей'
    text = forms.CharField(max_length=4096)
