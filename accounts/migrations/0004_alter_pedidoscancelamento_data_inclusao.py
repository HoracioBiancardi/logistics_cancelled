# Generated by Django 4.0.2 on 2022-02-08 12:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_pedidoscancelamento_id_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoscancelamento',
            name='data_inclusao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
