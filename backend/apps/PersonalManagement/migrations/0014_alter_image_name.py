# Generated by Django 4.1.7 on 2023-04-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalManagement', '0013_address_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]