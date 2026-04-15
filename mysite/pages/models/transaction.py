from django.db import models
from django.contrib.auth.models import User


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
    security = models.ForeignKey(
        'Security',
        on_delete=models.PROTECT,
        verbose_name='Ценная бумага'
    )
    transaction_type = models.CharField(
        max_length=4,
        choices=TRANSACTION_TYPES,
        verbose_name='Тип операции'
    )
    buy_quantity = models.PositiveIntegerField(
        verbose_name='Количество бумаг куплено'
    )
    buy_price_per_share = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Цена за бумагу при покупке'
    )
    buy_fee = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Комиссия покупки'
    )
    tmon_price_on_date = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Цена за бумагу TMON'
    )
    sell_quantity = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Количество бумаг продано'
    )
    sell_price_per_share = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Цена продажи'
    )
    sell_fee = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Комиссия продажи'
    )
    broker = models.ForeignKey(
        'Broker',
        on_delete=models.PROTECT,
        verbose_name='Брокер'
    )
    planned_sell_price = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Планируемая цена продажи'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_data',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Операция с ценной бумагой'
        verbose_name_plural = 'Операции с ценными бумагами'
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} {self.transaction_type} {self.buy_quantity} {self.security.ticker} от {self.transaction_date}, отображение на дашборде {self.is_on_dashboard}"
        # field_values = []
        # for field in self._meta.get_fields():
        #     field_values.append(str(getattr(self, field.name, '')))
        # return ' | '.join(field_values)