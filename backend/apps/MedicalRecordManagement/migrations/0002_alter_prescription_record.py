# Generated by Django 4.1.7 on 2023-04-22 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedicalRecordManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='record',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='MedicalRecordManagement.medicalrecord'),
        ),
    ]
