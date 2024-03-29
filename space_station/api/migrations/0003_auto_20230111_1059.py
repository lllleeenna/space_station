# Generated by Django 3.2.16 on 2023-01-11 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_rename_station_id_indication_station'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indication',
            name='axis',
            field=models.CharField(choices=[('x', 'x'), ('y', 'y'), ('z', 'z')], max_length=1, verbose_name='Координата'),
        ),
        migrations.AlterField(
            model_name='indication',
            name='distance',
            field=models.IntegerField(verbose_name='Смещение по координате'),
        ),
        migrations.AlterField(
            model_name='indication',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indication', to='api.station', verbose_name='Станция'),
        ),
        migrations.AlterField(
            model_name='indication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indication', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
