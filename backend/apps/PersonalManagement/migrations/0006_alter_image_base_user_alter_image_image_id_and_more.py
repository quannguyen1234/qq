# Generated by Django 4.1.7 on 2023-03-30 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PersonalManagement', '0005_alter_image_base_user_alter_image_image_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='base_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_id',
            field=models.CharField(default=uuid.uuid4, max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_type',
            field=models.IntegerField(choices=[(1, 'DoctorNotarizedImage')], max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.TextField(null=True),
        ),
    ]