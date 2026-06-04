from django.db import models

class Tickets(models.Model):
    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=40)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'{self.name} - {self.phone}'
