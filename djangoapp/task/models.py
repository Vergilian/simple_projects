from decimal import Decimal
from django.db import models

# Create your models here.
class Buyer(models.Model):
    name = models.CharField(max_length=100,unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    age = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    subscribe = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} (Возраст: {self.age}, Баланс: {self.balance}₽)'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Game(models.Model):
    title = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    age_limited = models.BooleanField('Buyer',default=False, blank=True)
    buyer = models.ManyToManyField('Buyer', related_name='games', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


