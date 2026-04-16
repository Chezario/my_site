from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from decimal import Decimal

from .t_invest_utils import get_current_price, get_stock_price, quotation_to_decimal
from .models import SecurityTransaction
from .token import INVEST_TOKEN
from .forms import MyForm

def plural_form(n, forms=('день', 'дня', 'дней')):
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
def dashboard(request):
    tfoot_data = {
        'result_summ': 0,
        'result_with_nalog_summ': 0,
        'quantity': 0
    }
    stock_filter = request.GET.get('category')
    categories = set(SecurityTransaction.objects.values_list('security__name', flat=True))
    if stock_filter:
        transactions = SecurityTransaction.objects.filter(is_on_dashboard=False, user=request.user, security__name=stock_filter)  # Получение записей из базы данных
    else:
        transactions = SecurityTransaction.objects.filter(is_on_dashboard=False, user=request.user)  # Получение записей из базы данных

    for transaction in transactions:
        transaction.result = (transaction.sell_price_per_share * transaction.sell_quantity) - transaction.sell_fee - (transaction.buy_price_per_share * transaction.buy_quantity) - transaction.buy_fee
        if transaction.result > 0:
            transaction.result_with_nalog = transaction.result * Decimal('0.87')
        else:
            transaction.result_with_nalog = transaction.result
        tfoot_data['result_summ'] += transaction.result
        tfoot_data['result_with_nalog_summ'] += transaction.result_with_nalog
        tfoot_data['quantity'] += transaction.buy_quantity
    context = {
        'transactions': transactions,
        'categories': categories,
        'tfoot_data': tfoot_data,
    }

    return render(request, 'dashboard.html', context=context)


@login_required
def index(request):
    TMON_FIGI = 'TCS70A106DL2'
    tfoot_data = {
        'current_summ': 0,
        'desired_summ': 0,
        'tmon_summ': 0,
        'quantity': 0
    }
    stock_filter = request.GET.get('category')
    categories = set(SecurityTransaction.objects.values_list('security__name', flat=True))
    if stock_filter:
        transactions = SecurityTransaction.objects.filter(is_on_dashboard=True, user=request.user, security__name=stock_filter)  # Получение записей из базы данных
    else:
        transactions = SecurityTransaction.objects.filter(is_on_dashboard=True, user=request.user)  # Получение записей из базы данных

    for transaction in transactions:
        transaction.current_price = get_current_price(transaction.security.ticker) # Добавление в объект из базы данных текущей цены
        transaction.real_price = transaction.buy_price_per_share * (1 + transaction.broker.fee)
        transaction.price_to_zero = transaction.buy_price_per_share * ((1 + transaction.broker.fee) / (1 - transaction.broker.fee))
        transaction.percent = (transaction.current_price - transaction.price_to_zero) / (transaction.price_to_zero / 100)
        transaction.sum = transaction.buy_price_per_share * transaction.buy_quantity
        if transaction.tmon_price_on_date:
            tmon_price = quotation_to_decimal(get_stock_price(TMON_FIGI))
            tmon_count = (transaction.real_price * transaction.buy_quantity) / transaction.tmon_price_on_date
            transaction.tmon_result = tmon_price * tmon_count - transaction.tmon_price_on_date * tmon_count
            tfoot_data['tmon_summ'] += transaction.tmon_result
        transaction.result = (transaction.current_price * transaction.buy_quantity) * Decimal('0.9992') - (transaction.buy_price_per_share * transaction.buy_quantity) - transaction.buy_fee
        transaction.desired_profit = (transaction.planned_sell_price * transaction.buy_quantity) * Decimal('0.9992') - (transaction.buy_price_per_share * transaction.buy_quantity) - transaction.buy_fee
        transaction.percent_for_desired = (transaction.planned_sell_price - transaction.price_to_zero) / (transaction.price_to_zero / 100)
        transaction.tmon_tod_price = quotation_to_decimal(get_stock_price(TMON_FIGI))
        tfoot_data['current_summ'] += transaction.result
        tfoot_data['desired_summ'] += transaction.desired_profit
        tfoot_data['quantity'] += transaction.buy_quantity

    context = {
        'transactions': transactions,
        'tfoot_data': tfoot_data,
        'categories': categories,
    }
    # content[name2] = {
    #     'name': name2,
    #     'date': '2026-03-23',
    #     'start_price': '315,86',
    #     'current_price': get_real_price(name2)
    # }
    return render(request, 'index.html', context)


@login_required
def my_form_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)  # Передаём данные POST в форму
        if form.is_valid():
            # Получаем данные из формы
            price = form.cleaned_data['price']
            date = form.cleaned_data['date']
            

            # Здесь ваша бизнес‑логика (сохранение в БД, отправка email и т. д.)
            print(f"Получены данные: {price}, {data}")
            context = {
                'data': [price, date]
            }

            # Перенаправление после успешной отправки
            return render(request, 'success.html', context=context)
    else:
        form = MyForm()  # Пустая форма для GET‑запроса

    return render(request, 'forms/my_form.html', {'form': form})


def operation_details(request, operation_id):
    operation = get_object_or_404(SecurityTransaction, id=operation_id)
    print(operation)
    context = {
        'operation': operation
    }
    return render(request, 'operation.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)