from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, date, timedelta


def check_time(time_object: timedelta):
    delta = timedelta(days=0, hours=0, minutes=0, seconds=0)
    if int(time_object.seconds / 3600) < 12:
        delta = timedelta(days=1)
    time_object -= delta
    return time_object


def index(request):
    current_date = datetime.now()
    custom_date = datetime(2026, 1, 1)
    delta = check_time(custom_date - current_date)
    content = {
        'title': 'Main Page',
        'content': 'Hello People',
        'days_left': int(delta.days),
    }
    return render(request, 'index.html', content)


if __name__ == '__main__':
    pass