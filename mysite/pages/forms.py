from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import UploadedFile


class MyForm(forms.Form):
    price = forms.DecimalField(label='Цена', max_digits=6, decimal_places=2)
    date = forms.DateField(
        # widget=forms.SelectDateWidget(
        #     years=range(2026, 2027)
        # ),
        # label='Дата',
        # required=False
        widget=AdminDateWidget(),
    )


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'file']