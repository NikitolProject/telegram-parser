import io
import asyncio
import threading

import imageio

from django.shortcuts import render, redirect

from app.forms import ParserForm, MailingForm
from app.tasks import start_parsing, start_mailing

from django.core.files.uploadedfile import InMemoryUploadedFile


def start_parse(request):
    if not request.POST or 'apply' not in request.POST:
        return redirect('admin:app_telegramchannel_changelist')
    
    form = ParserForm(request.POST)

    if not form.is_valid():
        return redirect('admin:app_telegramchannel_changelist')
        
    print(request.POST)

    start_background_parsing_loop(request, form)

    return render(request, 'admin/parser_confirm.html', context={})


def start_malling(request):
    if not request.POST or 'apply' not in request.POST:
        return redirect('admin:app_telegramuser_changelist')
    
    file = None

    if request.FILES:
        form = MailingForm(request.POST, request.FILES)
    else:
        form = MailingForm(request.POST)

    if not form.is_valid():
        return redirect('admin:app_telegramuser_changelist')
        
    print(request.POST)
    print(request.FILES)

    if request.FILES and form.cleaned_data['media'].content_type != "video/mp4":
        file = form.cleaned_data['media'].read()
    elif request.FILES and form.cleaned_data['media'].content_type == "video/mp4":
        print("process convert video to gif...")
        video = form.cleaned_data['media'].read()
        frames = imageio.mimread(video, plugin='pyav')

        gif_bytes = io.BytesIO()
        imageio.mimsave(gif_bytes, frames, format='gif')

        file = gif_bytes.getvalue()
        print("convert success")

    start_background_mailing_loop(request, form, file)

    return render(request, 'admin/malling_confirm.html', context={})


def start_background_parsing_loop(request, form):
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_async_parsing_loop, args=(loop, request, form))
    t.start()


def start_background_mailing_loop(request, form, file):
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_async_mailing_loop, args=(loop, request, form, file))
    t.start()


def run_async_parsing_loop(loop, request, form):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        start_parsing(
            [int(cid) for cid in request.POST['_selected_action']], 
            form.cleaned_data['post_count']
        )
    )
    loop.close()


def run_async_mailing_loop(loop, request, form, file):
    print(request.POST['_selected_action'])
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        start_mailing(
            request.POST['_selected_action'], 
            form.cleaned_data['text'], file
        )
    )
    loop.close()
