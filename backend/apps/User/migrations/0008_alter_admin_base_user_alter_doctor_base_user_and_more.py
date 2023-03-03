# Generated by Django 4.1.7 on 2023-03-01 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_alter_admin_admin_id_alter_doctor_doctor_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='base_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='base_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_doctor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patient',
            name='base_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_patient', to=settings.AUTH_USER_MODEL),
        ),
    ]
