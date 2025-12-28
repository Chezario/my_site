from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe


def plural_form(n, forms=('день', 'дня', 'дней')):
    # n = abs(n) % 100
    # n1 = n % 10
    
    if str(n)[-1] == '1':
        return forms[0]
    if 1 < int(str(n)[-1]) < 5:
        return forms[1]
    else:
        return forms[2]


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
        'data_base': [
            mark_safe(f'<b>{int(delta.days)} {plural_form(int(delta.days))} </b> осталось до нового года.'),
            datetime.now(),
            'Проверка карточек',
            f'Еще одна карточка',
        ],
    }
    return render(request, 'index.html', content)


if __name__ == '__main__':
    for i in range(11):
        print(plural_form(i))
