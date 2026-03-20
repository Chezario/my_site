from django.db import models


class Security(models.Model):
    # Идентификационные данные
    name = models.CharField(
        max_length=200,
        verbose_name='Полное наименование'
    )
    ticker = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Тикер'
    )
    isin = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name='ISIN-код'
    )

    # Тип и категория
    SECURITY_TYPES = [
        ('STOCK', 'Акция'),
        ('BOND', 'Облигация'),
        ('ETF', 'ETF'),
        ('DERIVATIVE', 'Дериватив'),
        ('OTHER', 'Другое'),
    ]
    type = models.CharField(
        max_length=10,
        choices=SECURITY_TYPES,
        verbose_name='Тип ценной бумаги'
    )

    # Стоимостные характеристики
    face_value = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Номинальная стоимость'
    )
    currency = models.CharField(
        max_length=3,
        default='RUB',
        verbose_name='Валюта номинала'
    )
    lot_size = models.PositiveIntegerField(
        default=1,
        verbose_name='Размер лота'
    )

    # Даты
    issue_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата выпуска'
    )
    maturity_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата погашения'
    )

    # Финансовые параметры (для облигаций)
    coupon_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Купонная ставка (%)'
    )
    yield_to_maturity = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name='Доходность к погашению (%)'
    )

    # Метаданные
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создана'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлена'
    )

    class Meta:
        verbose_name = 'Ценная бумага'
        verbose_name_plural = 'Ценные бумаги'
        indexes = [
            models.Index(fields=['ticker']),
            models.Index(fields=['isin']),
            models.Index(fields=['type']),
        ]
        ordering = ['ticker']

    def __str__(self):
        return f"{self.name} ({self.ticker})"