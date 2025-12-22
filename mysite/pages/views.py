from django.shortcuts import render
from django.http import HttpResponse
from datetime import date


def index(request):
    date1 = date.today()
    date2 = date.fromisoformat('2025-12-31') - date1
    content = {
        'title': 'Main Page',
        'content': 'Hello People',
        'days_left': int(date2.days),
    }
    return render(request, 'index.html', content)


