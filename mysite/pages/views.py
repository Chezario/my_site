from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .t_invest_utils import get_real_price
from .models import SecurityTransaction
import subprocess
import os
from .token import INVEST_TOKEN

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


@login_required
def index(request):

 

    # current_date = datetime.now()
    # custom_date = datetime(2026, 1, 1)
    # delta = check_time(custom_date - current_date)
    # content = [1, 2, 3, 4]
    # context = {
    #     'title': 'Main Page',
    #     'content': 'Hello People',
    #     'data_base': [
    #         mark_safe(f'<b>{int(delta.days)} {plural_form(int(delta.days))} </b> осталось до нового года.'),
    #         datetime.now(),
    #         'Проверка карточек',
    #         f'Еще одна карточка',
    #     ],
    # }
    # if current_date >= custom_date:
    #     content['data_base'][0] = 'Новый год наступил'
    # return render(request, 'index.html', context)
    return render(request, 'index.html')


if __name__ == '__main__':
    for i in range(11):
        print(plural_form(i))


@login_required
def dashboard(request):
    transactions = SecurityTransaction.objects.all()
    current_prices = {}
    for transaction in transactions:
        current_prices[transaction.security.name] = get_real_price(transaction.security.name)
        transaction['current_price'] = current_prices.get(transaction.security.name, 0)
        transaction['real_price'] = transaction.price_per_share * (1 + transaction.broker.fee)
        transaction['price_to_zero'] = transaction.price_per_share * ((1 + transaction.broker.fee) / (1 - transaction.broker.fee))
        transaction['percent'] = (transaction.price_per_share - transaction.real_price) / (transaction.price_per_share / 100)
    # for transaction in transactions:
    context = {
        'transactions': transactions,
        'current_prices': current_prices
    }
    # content[name2] = {
    #     'name': name2,
    #     'date': '2026-03-23',
    #     'start_price': '315,86',
    #     'current_price': get_real_price(name2)
    # }
    return render(request, 'dashboard.html', context)


# @login_required
# def dashboard(request):
#     transactions = SecurityTransaction.objects.all()
#     current_prices = {}
#     # for transaction in transactions:
#     #     current_prices[transaction.security.name] = get_real_price(transaction.security.name)
#     for transaction in transactions:
#         transaction.current_price = current_prices.get(transaction.security.name, 0)
#         transaction.real_price = transaction.price_per_share * (1 + transaction.broker.fee)
#         transaction.price_to_zero = transaction.price_per_share * ((1 + transaction.broker.fee) / (1 - transaction.broker.fee))
#     context = {
#         'transactions': transactions,
#         'current_prices': current_prices
#     }
#     # content[name2] = {
#     #     'name': name2,
#     #     'date': '2026-03-23',
#     #     'start_price': '315,86',
#     #     'current_price': get_real_price(name2)
#     # }
#     return render(request, 'dashboard.html', context)
