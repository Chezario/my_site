from django import forms

from .models import Tickets


class TicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ['name', 'phone', 'comment']
        labels = {
            'name': 'Ваше имя',
            'phone': 'Телефон',
            'comment': 'Пожелания',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Например, Олег'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
            'comment': forms.Textarea(attrs={'placeholder': '', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')