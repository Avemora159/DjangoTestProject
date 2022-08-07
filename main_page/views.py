from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from .forms import DateSelectionForm
import os
import json


def get_json(name):
    json_path = os.path.join(settings.STATIC_ROOT, name)
    with open(json_path, 'r') as data:
        json_ = json.load(data)
    return json_


@login_required(login_url='../authorization/')
def index(request):
    context = {}
    form = DateSelectionForm(request.POST or None)
    context['form'] = form
    context['json'] = get_json('json_today.json')
    if request.method == 'POST':
        if form.is_valid():
            form_data = form.cleaned_data.get("date")
            if form_data == '1':
                context['json'] = get_json('json_today.json')
            elif form_data == '2':
                context['json'] = get_json('json_yesterday.json')
            elif form_data == '3':
                context['json'] = get_json('json_week.json')
            elif form_data == '4':
                context['json'] = get_json('json_month.json')
            elif form_data == '5':
                context['json'] = get_json('json_year.json')
    return render(request, 'main_page/index.html', context)
