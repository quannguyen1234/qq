# Generated by Django 4.1.7 on 2023-04-22 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedicalRecordManagement', '0002_alter_prescription_record'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='record',
        ),
    ]
