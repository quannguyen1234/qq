# Generated by Django 4.1.7 on 2023-03-29 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0018_alter_baseuser_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='notarized_image',
        ),
    ]
