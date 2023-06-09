# Generated by Django 4.1.7 on 2023-05-10 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0004_diagnosticbill_diagnostic_form'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='diagnosticbilldetail',
            constraint=models.CheckConstraint(check=models.Q(('distance__gte', 0)), name='distance_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='diagnosticbilldetail',
            constraint=models.CheckConstraint(check=models.Q(('doctor_fee__gte', 0)), name='doctor_fee_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='diagnosticbilldetail',
            constraint=models.CheckConstraint(check=models.Q(('total_fee__gte', 0)), name='total_fee_gte_0'),
        ),
    ]
