# Generated by Django 4.1.7 on 2023-04-20 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonalManagement', '0020_alter_imagedepartment_image_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaldepartment',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
