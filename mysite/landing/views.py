from django.shortcuts import render, redirect
from .forms import TicketForm


def index(request):
    form = TicketForm(request.POST or None)

    if request.method == 'POST':
        form = TicketForm(request.POST)
        form.save()
        # messages.success(request, 'Заявка сохранена. Мы свяжемся с вами по телефону.')
        return redirect('landing:index')
    context = {
        "form": form,
    }
    return render(request, 'landing/index.html', context)