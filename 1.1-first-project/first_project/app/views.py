import os
import datetime
from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'

    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)


# noinspection PyUnusedLocal
def time_view(request):
    current_time = datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


# noinspection PyUnusedLocal
def workdir_view(request):
    try:
        directory_content = os.listdir('.')
        formatted_content = '<br>'.join(directory_content)
        msg = f'Содержимое рабочей директории:<br><br>{formatted_content}'
    except Exception as error:
        msg = f'Произошла ошибка при сканировании директории: {error}'

    return HttpResponse(msg)
