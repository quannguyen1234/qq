# Generated by Django 4.1.7 on 2023-04-11 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0003_alter_connectdoctor_patient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectdoctor',
            name='is_confirm',
            field=models.BooleanField(default=False),
        ),
    ]
