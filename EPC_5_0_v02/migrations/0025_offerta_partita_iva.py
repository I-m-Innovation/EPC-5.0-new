# Generated by Django 5.1.3 on 2024-11-13 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EPC_5_0_v02', '0024_offerta_delta_totale_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerta',
            name='partita_iva',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
