# Generated by Django 4.1.7 on 2023-05-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0005_diagnosticbilldetail_distance_gte_0_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosticbill',
            name='diagnostic_form',
            field=models.IntegerField(choices=[(0, 'ONLINE'), (1, 'OFLINE')]),
        ),
    ]
