# Generated by Django 4.1.7 on 2023-04-14 01:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PersonalManagement', '0017_alter_address_base_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='ImageUser',
        ),
        migrations.AlterModelTable(
            name='imageuser',
            table='ImageUser',
        ),
    ]
