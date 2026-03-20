from django.db import models

class SecurityTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Покупка'),
        ('SELL', 'Продажа'),
    ]

    is_on_dashboard = models.BooleanField(
        default=True,
        verbose_name='Отображать на дашборде',
        help_text='Отметьте, чтобы товар/статья отображалась на дашборде'
    )

    transaction_date = models.DateTimeField(
        verbose_name='Дата и время операции'
    )
    security = models.CharField(
        max_length=100,
        verbose_name='Название ценной бумаги'
    )
    ticker = models.CharField(
        max_length=20,
        verbose_name='Тикер'
    )
    transaction_type = models.CharField(
        max_length=4,
        choices=TRANSACTION_TYPES,
        verbose_name='Тип операции'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество бумаг'
    )
    price_per_share = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Цена за бумагу'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Общая сумма операции'
    )
    sell_price_per_share = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Цена продажи'
    )
    sell_quantity = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Количество проданных бумаг'
    )
    broker = models.ForeignKey(
        'Broker',
        on_delete=models.PROTECT,
        verbose_name='Брокер'
    )
    security = models.ForeignKey(
        'Security',
        on_delete=models.PROTECT,
        verbose_name='Ценная бумага'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Примечания'
    )

    class Meta:
        verbose_name = 'Операция с ценной бумагой'
        verbose_name_plural = 'Операции с ценными бумагами'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.ticker} от {self.transaction_date}"
