# Generated by Django 5.1.3 on 2024-11-14 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EPC_5_0_v02', '0025_offerta_partita_iva'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerta',
            name='user',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
