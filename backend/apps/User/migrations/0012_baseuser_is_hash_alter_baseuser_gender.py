# Generated by Django 4.1.7 on 2023-03-20 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_alter_baseuser_firstname_alter_baseuser_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_hash',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='gender',
            field=models.BooleanField(choices=[(2.0, 'Other'), (0, 'Male'), (1, 'Female')], null=True),
        ),
    ]
