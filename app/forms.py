from django import forms


class ParserForm(forms.Form):
    title = 'Запуск парсера для сбора пользователей'
    post_count = forms.IntegerField()


class MailingForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    title = 'Запуск рассылки на выбранных пользователей'
    text = forms.CharField(max_length=4096, widget=forms.Textarea)
    media = forms.FileField(required=False)
