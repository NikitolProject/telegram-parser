from django import forms


class ParserForm(forms.Form):
    title = 'Запуск парсера для сбора пользователей'
    post_count = forms.IntegerField()
