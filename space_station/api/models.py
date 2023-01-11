from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Station(models.Model):
    """Модель станции."""

    class ChoicesCondition(models.TextChoices):
        RUNING = ('runing', 'запущена')
        BROKEN = ('broken', 'сломана')

    name = models.CharField('Название станции', max_length=50)
    condition = models.CharField(
        max_length=10,
        choices=ChoicesCondition.choices,
        default=ChoicesCondition.RUNING,
        verbose_name='Состояние',
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
    )
    broken_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата поломки',
    )
    x = models.IntegerField(default=100)
    y = models.IntegerField(default=100)
    z = models.IntegerField(default=100)


class Indication(models.Model):
    """Модель указания для отслеживания изменения положения станции."""

    class ChoicesAxis(models.TextChoices):
        X = ('x', 'x')
        Y = ('y', 'y')
        Z = ('z', 'z')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='indication',
        verbose_name='Пользователь',
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='indication',
        verbose_name='Станция',
    )
    axis = models.CharField(
        max_length=1,
        choices=ChoicesAxis.choices,
        verbose_name='Координата',
    )
    distance = models.IntegerField(
        verbose_name='Смещение по координате',
    )
