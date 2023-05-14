# Generated by Django 4.1.7 on 2023-05-14 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0005_connectdoctor_fee'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='connectdoctor',
            constraint=models.UniqueConstraint(fields=('doctor', 'patient'), name='unique_conversation'),
        ),
    ]
