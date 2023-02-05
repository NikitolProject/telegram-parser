import asyncio
import threading

from django.shortcuts import render, redirect

from app.forms import ParserForm
from app.tasks import start_parsing


def start_parse(request):
    if not request.POST or 'apply' not in request.POST:
        return redirect('admin:app_telegramchannel_changelist')
    
    form = ParserForm(request.POST)

    if not form.is_valid():
        return redirect('admin:app_telegramchannel_changelist')
        
    print(request.POST)

    start_background_loop(request, form)

    return render(request, 'admin/parser_confirm.html', context={})


def start_background_loop(request, form):
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_async_loop, args=(loop, request, form))
    t.start()


def run_async_loop(loop, request, form):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        start_parsing(
            [int(cid) for cid in request.POST['_selected_action']], 
            form.cleaned_data['post_count']
        )
    )
    loop.close()
