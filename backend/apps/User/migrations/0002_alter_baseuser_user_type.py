# Generated by Django 4.1.7 on 2023-02-28 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='user_type',
            field=models.SmallIntegerField(choices=[('Doctor', 0), ('Patient', 1), ('Admin', 2)], null=True),
        ),
    ]
