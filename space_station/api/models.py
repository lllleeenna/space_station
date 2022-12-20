from django.contrib.auth import get_user_model
from django.db import models

CHOICES_CONDITION = (
    ('runing', 'запущена'),
    ('broken', 'сломана')
)

CHOICES_AXIS = (
    ('x', 'x'),
    ('y', 'y'),
    ('z', 'z')
)


User = get_user_model()


class Station(models.Model):
    """Модель станции."""
    name = models.CharField('Название станции', max_length=50)
    condition = models.CharField(
        'Состояние',
        max_length=10,
        default='runing',
        choices=CHOICES_CONDITION,
    )
    create_date = models.DateTimeField(
        'Дата создания', auto_now_add=True, db_index=True
    )
    broken_date = models.DateTimeField('Дата поломки', null=True, blank=True)
    x = models.IntegerField(default=100)
    y = models.IntegerField(default=100)
    z = models.IntegerField(default=100)


class Indication(models.Model):
    """Модель указания для отслеживания изменения положения станции."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='indication'
    )
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name='indication'
    )
    axis = models.CharField(max_length=1, choices=CHOICES_AXIS)
    distance = models.IntegerField()
