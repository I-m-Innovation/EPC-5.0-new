# Generated by Django 5.1.3 on 2024-11-12 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EPC_5_0_v02', '0019_offerta_delta_leasing_decimo_anno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerta',
            name='delta_totale',
            field=models.FloatField(null=True),
        ),
    ]
