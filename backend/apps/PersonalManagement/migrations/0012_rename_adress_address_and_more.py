# Generated by Django 4.1.7 on 2023-04-03 16:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PersonalManagement', '0011_adress'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Adress',
            new_name='Address',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='adress_id',
            new_name='address_id',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='adress_type',
            new_name='address_type',
        ),
    ]
