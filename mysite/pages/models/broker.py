from django.db import models


class Broker(models.Model):
    BROKER_NAME = [
        ('SBER', 'Сбербанк'),
        ('T', 'Т-банк'),
    ]

    name = models.CharField(
        max_length=100,
        choices=BROKER_NAME,
        verbose_name='Название брокера'
    )
    fee = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        verbose_name='Комиссия брокера'
    )
    exchange_fee = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        verbose_name='Комиссия биржи'
    )

    class Meta:
        verbose_name = 'Брокер'
        verbose_name_plural = 'Брокеры'

    def __str__(self):
        return f"{self.name} комиссия брокера ({self.fee}), комиссия биржи ({self.exchange_fee})"